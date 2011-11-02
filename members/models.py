from django.db import models
from datetime import date, datetime, timedelta
from decimal import Decimal
import math

CASH_PAYMENT='C'
BANK_PAYMENT='B'
GRATIS='G'

PAYMENT_TYPE = [
    ('C', 'Cash'),
    ('B', 'Bank Transfer'),
    ('G', 'Gratis')
]

DAYS_PER_MONTH=365.25/12
def delta_months(months):
    """ Make a datetime timedelta for this many months"""
    return timedelta(DAYS_PER_MONTH*months)


class Member(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    join_date = models.DateField()
    address = models.TextField()
    username = models.CharField(max_length=20, blank=True)
    emergency_contact_name = models.CharField(max_length=50)
    emergency_contact_number = models.CharField(max_length=50)
    medical_info = models.TextField(blank=True)

    def __unicode__(self):
        return self.fullname()

    def fullname(self):
        return "%s %s" % (self.first_name, self.last_name)

    def expiry_date(self):
        """
        Return the expiry date for this member's full or associate membership
        """
        payments = self.memberpayment_set.order_by("-date")
        # walk backwards through payments until we find a start
        months = 0
        start = self.join_date
        for payment in payments:
            months += payment.duration()
            if not payment.continues_membership: # beginning
                start = payment.date
                break
        return start + delta_months(months)

    def member_type(self):
        """
        Return the current member type, or Casual if the membership has expired
        """
        payments = self.memberpayment_set.order_by("-date")
        if len(payments) == 0 or self.expiry_date() < date.today():
            return Membership.objects.get(membership_name="Casual")
        else:
            return payments[0].membership_type


class Email(models.Model):
    member = models.ForeignKey(Member)
    email = models.CharField(max_length=50)
    is_preferred = models.BooleanField(default=True)

class Expense(models.Model):
    via_member = models.ForeignKey(Member, null=True, blank=True)
    description = models.TextField()
    expense_value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    payment_type = models.CharField(max_length=1, choices=PAYMENT_TYPE)

class RecurringExpense(Expense):
    PERIOD=[
        ("Year", "Year"),
        ("Month", "Month"),
        ("Day",   "Day"),
        ]
    period_unit = models.TextField(choices=PERIOD)
    period = models.IntegerField()
    end_date = models.DateField(null=True, blank=True)

class Income(models.Model):
    description = models.TextField(blank=True)
    from_member = models.ForeignKey(Member, null=True, blank=True)
    payment_type = models.TextField(choices=PAYMENT_TYPE)
    payment_value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

class Membership(models.Model):
    membership_name = models.CharField(max_length=30)
    membership_description = models.TextField(blank=True)

    def __unicode__(self):
        return self.membership_name

class MemberPayment(models.Model):
    """
    Any payment (or freebie) for an Associate or Full membership
    """
    member = models.ForeignKey(Member)
    membership_type = models.ForeignKey(Membership)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE)
    payment_value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    # only set this for freebies, is calculated from payment_value otherwise
    free_months = models.IntegerField(default=0)
    continues_membership = models.BooleanField()

    def duration(self):
        """ Calculate how many months of the given membership this buys
            (can be fractional)
        """
        return MembershipCost.objects.applicable_duration(self.membership_type,
                                                          self.date,
                                                          self.payment_value)

class CostManager(models.Manager):
    def applicable_cost(self, membership_type, date=date.today()):
        """
        Return the monthly cost applicable for a particular membership type, on a particular day
        """
        costs = self.filter(membership=membership_type, valid_from__lte=date).order_by("-valid_from")
        if costs.count() == 0:
            return None
        else:
            return costs[0]


    def applicable_duration(self, membership_type, date, payment):
        """
        Return the amount of time a payment is good for (in fractional months),
        given a particular starting date and duration. Will pro rata across discounted rates.
        """
        payment=float(payment)
        starter = self.applicable_cost(membership_type, date) # rate applying at start
        changes = self.filter(membership=membership_type,
                              valid_from__gt=date).order_by("valid_from") # rates applying thereafter
        changes = [starter] + list(changes)
        cost = float(starter.monthly_cost)
        total = 0.0
        for fr,to in ( (changes[i],changes[i+1]) for i in range(0,len(changes)-1) ):
            period=to.valid_from-max(fr.valid_from, date)
            period_months = float(period.days)/DAYS_PER_MONTH
            cost = min(float(fr.monthly_cost), cost)
            period_cost = period_months*cost
            if period_cost > payment:
                # this is more than our outstanding amount, so we're done
                return total + payment/cost
            else:
                total += period_months
                payment -= period_cost
        # at end of list, so remainder is charged out at whatever rate applies at end
        return total + payment/min(cost, float(changes[-1].monthly_cost))


class MembershipCost(models.Model):
    membership = models.ForeignKey(Membership)
    monthly_cost = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateField()
    objects = CostManager()

class Phone(models.Model):
    member = models.ForeignKey(Member)
    phone_number = models.CharField(max_length=20)
    description = models.TextField(blank=True)

