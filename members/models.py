from datetime import date, timedelta
import logging

from django.db import models
from django.core.cache import cache

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context


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

class Member(models.Model):
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    join_date = models.DateField(verbose_name="Date Joined")
    address = models.TextField(verbose_name="Address", help_text="A postal address where you can be reached")
    username = models.CharField(max_length=20, blank=True, verbose_name="Website Username",
                                help_text="Username on www.makehackvoid.com (if you have one.)")
    emergency_contact_name = models.CharField(max_length=50, verbose_name="Emergency Contact Name")
    emergency_contact_number = models.CharField(max_length=50, verbose_name="Emergency Contact Phone Number")
    medical_info = models.TextField(blank=True, verbose_name="Medical Information",
                                    help_text="Any medical information that's pertinent to your time in the space?")

    def __unicode__(self):
        return self.fullname()

    def fullname(self):
        return "%s, %s" % (self.last_name, self.first_name)

    def expiry_date(self):
        """
        Return the expiry date for this member's full or associate membership
        """
        cached = cache.get("membershipexpiry-%d" % self.id)
        if cached is not None:
            return cached

        payments = self.memberpayment_set.order_by("date")
        # walk forwards through payments, tracking expiration
        months = 0.0
        start = self.join_date
        last_type = None
        for payment in payments:
            if payment.duration() is None:
                continue
            if payment.is_existing_upgrade: # membership type is changing with this one
                # convert any outstanding months into months @ the new rate
                old_expiry = start + delta_months(months)
                remaining = old_expiry - payment.date # time remaining on the old rate, to be converted to new rate
                old_rate = MembershipCost.objects.applicable_rate(last_type, payment.date).monthly_cost
                new_rate = MembershipCost.objects.applicable_rate(payment.membership_type, payment.date).monthly_cost
                months = delta_to_months(remaining) * float(old_rate)/ float(new_rate)  # adjust by ratio of old:new rates
                start = payment.date
            elif not payment.continues_membership: # beginning anew
                start = payment.date
                months = 0.0

            months += MembershipCost.objects.applicable_duration(payment.membership_type,
                                                                     start + delta_months(months),
                                                                     payment.payment_value)
            last_type = payment.membership_type
            if payment.free_months:
                months += payment.free_months

        result = start + delta_months(months)
        cache.set("membershipexpiry-%d" % self.id, result)
        return result

    def member_type(self, at_date=date.today()):
        """
        Return the current member type, or Casual if the membership has expired
        """
        payments = self.memberpayment_set.order_by("-date")
        if len(payments) == 0 or self.expiry_date() < at_date:
            return Membership.objects.get(membership_name=settings.DEFAULT_MEMBERSHIP_NAME)
        else:
            return payments[0].membership_type


    def send_email(self, template, send_to_member=True):
        """
        Send the member an email, using the specified template for content
        """
        text = get_template("email/%s"%template).render(Context({"m":self}))
        subject = settings.EMAIL_SUBJECTS[template]
        recipients = []
        if send_to_member:
            emails = list(self.email_set.all())
            recipients = [ e.email for e in emails if e.is_preferred ]
            if len(recipients) == 0:
                recipients = [ e.email for e in emails ]
        if template in settings.EMAIL_CC:
            recipients += settings.EMAIL_CC[template]
        logger.info("Emailing template %s to %s for member id %s" % (template, recipients, self.id))
        if len(recipients) == 0:
            logger.info("No recipients, so no email!")
            return
        if settings.IS_DEVELOPMENT:
            logger.debug("Email not sent, body would be:\n%s" % text)
        else:
            send_mail(subject, text, settings.EMAIL_SENDER, recipients)

    class Meta:
        ordering = ["last_name", "first_name"]

    def save(self):
        if self.id:
            cache.delete("membershipexpiry-%d" % self.id)
        models.Model.save(self)


class Email(models.Model):
    member = models.ForeignKey(Member)
    email = models.CharField(max_length=50, verbose_name="Email Address")
    is_preferred = models.BooleanField(default=True, verbose_name="Preferred Address",
                                       help_text="Is this the address you'd rather be contacted on?")

class Membership(models.Model):
    membership_name = models.CharField(max_length=30)
    membership_description = models.TextField(blank=True)

    def __unicode__(self):
        return self.membership_name

class CostManager(models.Manager):

    def cached_costs(self, membership_type):
        """
        Return a (cached, if possible) list of all membership costs for a particular membership type,
        in chronological (first first) order
        """
        key = "membershipcosts-%d" % membership_type.id
        result = cache.get(key)
        if result is None:
            result = self.filter(membership=membership_type).order_by("valid_from")
            cache.set(key, result)
        return result

    def applicable_rate(self, membership_type, date=date.today()):
        """
        Return the monthly cost applicable for a particular membership type, on a particular day
        """
        costs = [ x for x in self.cached_costs(membership_type) if x.valid_from <= date ]
        return None if len(costs) == 0 else costs[-1]

    def applicable_duration(self, membership_type, date, payment):
        """
        Return the amount of time a payment is good for (in months, as a float)
        given a particular starting date and duration. Will pro rata across discounted rates.
        """
        payment=float(payment)
        starter = self.applicable_rate(membership_type, date) # rate applying at start
        if starter is None:
            raise Error("Asked to get applicable cost for %s at %s - no rate for membership applied then!" %
                        (membership_type, date))

        changes = [ x for x in self.cached_costs(membership_type) if x.valid_from > date ]
        changes = [starter] + list(changes)
        cost = float(starter.monthly_cost)
        total = 0.0
        for fr,to in ( (changes[i],changes[i+1]) for i in range(0,len(changes)-1) ):
            period=to.valid_from-max(fr.valid_from, date)
            period_months = delta_to_months(period)
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

    def save(self):
        cache.clear()
        models.Model.save(self)

    class Meta:
        ordering = [ "valid_from" ]

class Phone(models.Model):
    member = models.ForeignKey(Member)
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number")
    description = models.CharField(blank=True, max_length=80, verbose_name="Phone Number Description",
                                   help_text="Any description of this phone number?")

