from datetime import date, timedelta
import logging

from django.db import models
from django.core.cache import cache

from members.models import *

logger = logging.getLogger(__name__)

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

CASH_PAYMENT='C'
BANK_PAYMENT='B'
GRATIS='G'

PAYMENT_TYPE = [
    ('C', 'Cash Transfer'),
    ('B', 'Electronic Transfer'),
    ('G', 'Gratis')
]

DAYS_PER_MONTH=365.25/12
def delta_months(months):
    """ Make a datetime timedelta for this many months"""
    return timedelta(DAYS_PER_MONTH*months)

def delta_to_months(delta):
    return float(delta.days)/DAYS_PER_MONTH

class ExpenseManager(models.Manager):

    def all_expenses_for_period(self, from_date, to_date):
        """
        Return a list of all expenses for a given date - both simple single Expenses
        and RecurredExpenses

        Data comes back sorted by date, can't do sorting in DB because not all info is there.
        """
        simple = list(self.filter(date__gte=from_date,
                             date__lte=to_date).order_by("date"))
        recurring = list(RecurringExpense.objects.all().order_by("date"))

        # this is a bodgy hack to deal with model inheritance (remove any recurring ids)
        # there is probably a better way to do this
        recurring_ids = set([ r.id for r in recurring ])
        simple = [ s for s in simple if s.id not in recurring_ids ] # remove recurring

        for r in recurring:
            simple += r.expenses_for_period(from_date,to_date)
        return sorted(simple, key=lambda e:e.date)

    def balance_at_date(self, at_date):
        expenses = list(Expense.objects.all_expenses_for_period(date(2010,1,1), at_date))
        income = list(Income.objects.filter(date__lt=at_date))
        memberpayments = list(MemberPayment.objects.filter(date__lt=at_date))
        return sum(p.payment_value for p in memberpayments + income) - sum(e.payment_value for e in expenses)


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=30)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = [ "name" ]
        verbose_name_plural = "Expense Categories"


class Expense(models.Model):
    via_member = models.ForeignKey(Member, null=True, blank=True)
    description = models.TextField()
    payment_value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    payment_type = models.CharField(max_length=1, choices=PAYMENT_TYPE)
    category = models.ForeignKey(ExpenseCategory)

    objects = ExpenseManager()

    def __unicode__(self):
        return "%s -$%s %s %s" % (self.date, self.payment_value, self.category.name, self.description)

    class Meta:
        ordering = [ "-date" ]

class RecurringExpense(Expense):
    PERIOD=[
        ("Year", "Year"),
        ("Month", "Month"),
        ("Day",   "Day"),
        ]
    period_unit = models.CharField(max_length=10, choices=PERIOD)
    period = models.IntegerField()
    end_date = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return "Recurring Expense %s->%s $%s '%s'" % (self.date,
                                                      self.end_date if self.end_date is not None
                                                      else "",
                                                      self.payment_value, self.description)

    def expenses_for_period(self, start=None, end=None):
        """
        Return all of the payment dates for a particular period, as a list of RecurredExpenses
        """
        return list(self._expenses_for_period(start, end))

    def _expenses_for_period(self, start=None, end=None):
        """
        Return expenses for period as generator. Is wrapped into a list by expenses_for_period.
        """
        if end is not None and start is not None and end < start:
            raise Error("RecurringExpense expenses_for_period end must be after start")
        if start is None:
            start = self.date
        if end is None:
            end = self.end_date+timedelta(days=1)
        if end is None:
            raise Error("Cannot get RecurringExpense over an open-ended period")
        if self.period == 0:
            raise Error("RecurringExpense must have a non-zero period count")

        if self.end_date is not None:
            end = min(end, self.end_date+timedelta(days=1))

        def fixup_date(year, month, day):
            if month > 12:
                return fixup_date(year+1, month-12, day)
            try:
                return date(year, month, day)
            except ValueError as e:
                if day > 1:
                    return fixup_date(year,month,day-1)
                else:
                    raise e

        def get_iteration(n):
            d = self.date
            return {
                "Year" :  fixup_date(d.year+self.period*n,d.month,d.day),
                "Month" : fixup_date(d.year,d.month+self.period*n,d.day),
                "Day" :   d + timedelta(days=self.period*n),
                }[self.period_unit]

        for n in xrange(1000000):
            current = get_iteration(n)
            if current >= end:
                return
            elif current >= start:
                yield RecurredExpense(via_member=self.via_member,
                                      description=self.description,
                                      payment_value=self.payment_value,
                                      date=current,
                                      payment_type=self.payment_type,
                                      category=self.category)


class RecurredExpense(Expense):
    """
    A dummy class for expenses generated from a RecurringExpense, with same fields as
    Expense but not to be saved to a real database
    """
    def save(self):
        raise Error("A RecurredExpense is read-only from a RecurringExpense and cannot be saved")
    class Meta:
        managed = False # no db table for this one
        proxy = True

class BaseIncome(models.Model):
    """
    Any payment received
    """
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE)
    payment_value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __unicode__(self):
        return "%s $%s" % (self.date, self.payment_value)

    class Meta:
        abstract = True
        ordering = [ "-date" ]

class IncomeCategory(models.Model):
    name = models.CharField(max_length=30)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = [ "name" ]
        verbose_name_plural = "Income Categories"


class Income(BaseIncome):
    """
    Any payment received which is not for a member
    """
    description = models.TextField()
    category = models.ForeignKey(IncomeCategory)

    def __unicode__(self):
        return "%s $%s (%s %s)" % (self.date, self.payment_value, self.category.name, self.description)


class Product(models.Model):
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __unicode__(self):
            return self.name


class ExpiringProduct(Product):
    duration = models.PositiveIntegerField()
    duration_type = models.CharField(max_length=32,
                                     choices=[
                                     ("day", "Days"),
                                     ("week", "Weeks"),
                                     ("month", "Months"),
                                     ("year", "Years"),
                                     ])


class MembershipProduct(ExpiringProduct):
    membership = models.ForeignKey(Membership)


class MemberPayment(BaseIncome):
    member = models.ForeignKey(Member)
    product = models.ForeignKey(Product)

    def __unicode__(self):
        return "Payment $%s %s from %s (%s)" % (self.payment_value, self.date,
                                                self.member, self.product)

class ExpiringMemberPayment(BaseIncome):
    member = models.ForeignKey(Member)
    product = models.ForeignKey(ExpiringProduct)
    continues_previous = models.BooleanField()

    def __unicode__(self):
        return "Payment $%s %s from %s (%s)" % (self.payment_value, self.date,
                                                self.member, self.product)

class LegacyMemberPayment(BaseIncome):
    """
    Any payment (or freebie) for an Associate or Full membership
    """
    member = models.ForeignKey(Member)
    membership_type = models.ForeignKey(LegacyMembership)
    # only set this for freebies, is calculated from payment_value otherwise
    free_months = models.IntegerField(default=0)
    continues_membership = models.BooleanField(default=True, help_text="Is this a renewal (ie continues from current expiry date?)")
    is_existing_upgrade = models.BooleanField(default=False, verbose_name="Existing Member Changing Type",
                                              help_text="Is this an existing member changing membership type (meaning pro rata of any remaining time on their old type)")

    def duration(self):
        """ Calculate how many months of the given membership this buys
            (can be fractional)
        """
        return LegacyMembershipCost.objects.applicable_duration(self.membership_type,
                                                          self.date,
                                                          self.payment_value)

    def __unicode__(self):
        return "Payment $%s %s from %s (%s)" % (self.payment_value, self.date,
                                                self.member, self.membership_type)

    def save(self):
        old_id = self.id
        cache.delete("membershipexpiry-%d" % self.member.id)
        BaseIncome.save(self)
        if old_id is None and date.today() - self.date < timedelta(days=30): # new payment entered
            if self.member.memberpayment_set.count() == 1:
                self.member.send_email("welcome.txt")
            else:
                self.member.send_email("renewed.txt")

    class Meta:
        ordering = [ "-date" ]