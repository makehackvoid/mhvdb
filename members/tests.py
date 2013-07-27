"""
Run "manage.py test members" to test the members app
'./manage.py test members --traceback' gives a full traceback
In django 1.5 running 'manage.py test' will try to run the django-evolution tests which fail
"""

from datetime import date

from django.test import TestCase

from members.models import *
from finance.models import *


def dummy_member(name):
    """
    Utility function to make a dummy member
    """
    return Member(last_name=name.split(" ")[1],
                  first_name=name.split(" ")[0],
                  join_date=date(1995, 1, 1),
                  address="Test Lane",
                  emergency_contact_name="TestContact",
                  emergency_contact_number="5551234",
                  medical_info="Is a test case, DNR"
                  )


class LegacyMembershipExpiryTest(TestCase):
    """
    Test cases form embership expiries
    """

    def setUp(self):
        self.fred = dummy_member("Fred Durst")
        self.fred.save()

        # Membership type structure
        self.associate = LegacyMembership(membership_name="Associate")
        self.full = LegacyMembership(membership_name="Full")
        self.associate.save()
        self.full.save()

        # Dummy membership cost structure - associate went up 1 June 2011, full came down(!)
        LegacyMembershipCost(membership=self.associate, monthly_cost="20", valid_from=date(2011, 1, 1)).save()
        LegacyMembershipCost(membership=self.associate, monthly_cost="40", valid_from=date(2011, 6, 1)).save()
        LegacyMembershipCost(membership=self.full, monthly_cost="100", valid_from=date(2011, 1, 1)).save()
        LegacyMembershipCost(membership=self.full, monthly_cost="50", valid_from=date(2011, 6, 1)).save()

    def test_durations(self):
        """
        Test that the system knows what membership costs on various dates
        """
        self.assertEqual(LegacyMembershipCost.objects.applicable_rate(self.associate, date(2011, 2, 1)).monthly_cost, 20)
        self.assertEqual(LegacyMembershipCost.objects.applicable_rate(self.associate, date(2011, 7, 1)).monthly_cost, 40)
        self.assertEqual(LegacyMembershipCost.objects.applicable_rate(self.full, date(2012, 1, 1)).monthly_cost, 50)

    def test_auto_duration(self):
        """
        If a new LegacyMemberPayment gets inserted, its duration (if empty) should automatically be
        calculated based on the cost that applies at the time
        """
        payment = LegacyMemberPayment(membership_type=self.associate, payment_type=BANK_PAYMENT,
                                member=self.fred, payment_value="480", date=date(2011, 8, 1),
                                continues_membership=False)  # $40/mo * 12 months
        payment.save()
        payment = self.fred.legacymemberpayment_set.all()[0]
        self.assertEqual(payment.duration(), 12)
        self.assertEqual(self.fred.membership_expiry_date(), date(2012, 7, 31))

    def test_renewal_before_expiry(self):
        """
        If a member renews before their membership expires, the expiry date should be added to the end
        of their existing membership period
        """
        LegacyMemberPayment(membership_type=self.associate, payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="120", date=date(2011, 8, 1),
                      continues_membership=False).save()  # $40/mo * 3 months
        LegacyMemberPayment(membership_type=self.associate, payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="120", date=date(2011, 10, 1),
                      continues_membership=True).save()   # 3 more months
        self.assertEqual(self.fred.membership_expiry_date(), date(2012, 1, 30))

    def test_renewal_after_expiry(self):
        """
        If a member renews after their expiry date, but didn't stop their membership, the renewal
        payment should be backdated
        """
        LegacyMemberPayment(membership_type=self.associate, payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="120", date=date(2011, 8, 1),
                      continues_membership=False).save()  # $40/mo * 3 months
        LegacyMemberPayment(membership_type=self.associate, payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="120", date=date(2011, 12, 1),
                      continues_membership=True).save()   # 3 more months, LATE!
        self.assertEqual(self.fred.membership_expiry_date(), date(2012, 1, 30))

    def test_break_in_membership(self):
        """
        If a member lapses back to casual, then starts again, then their new membership doesn't
        count back to the old one
        """
        LegacyMemberPayment(membership_type=self.associate, payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="120", date=date(2011, 8, 1),
                      continues_membership=False).save()  # $40/mo * 3 months
        LegacyMemberPayment(membership_type=self.associate, payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="120", date=date(2012, 8, 1),
                      continues_membership=False).save()  # 3 months again
        self.assertEqual(self.fred.membership_expiry_date(), date(2012, 10, 31))

    def test_pro_rata_over_rate_reduction(self):
        """
        If the membership rate goes down during a membership, the membership
        should be pro rata extended to match the new value
        """

        # $200 buys 2 months on 1 May, but would buy 4 months on 1 June... so result
        # should be 3 months
        LegacyMemberPayment(membership_type=self.full, payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="200", date=date(2011, 5, 1),
                      continues_membership=False).save()
        self.assertEqual(self.fred.membership_expiry_date(), date(2011, 7, 30))

    def test_no_pro_rate_over_rate_hike(self):
        """
        OTOH, if the membership rate goes up during a membership, it's a bit rich to ask
        for it to be pro rataed shorter - so we don't do that
        """

        # $120 buys 6 months on 1 May, and that's how it stays
        LegacyMemberPayment(membership_type=self.associate, payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="120", date=date(2011, 5, 1),
                      continues_membership=False).save()
        self.assertEqual(self.fred.membership_expiry_date(), date(2011, 10, 30))

    def test_pro_rata_applies_renewals_equally(self):
        """
        If someone renews late then their pro rata should apply the same
        as someone who renews on time
        """
        jane = dummy_member("Jane Durst")
        jane.save()

        # $200 buys 2 months on 1 May, but would buy 4 months on 1 June...
        # so expectation is:
        # $200 on 1 March buys to 1 May
        # $200 on 1 May is $100 to 1 June, then $100 more to 1 August
        LegacyMemberPayment(membership_type=self.full, payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="200", date=date(2011, 3, 1),
                      continues_membership=False).save()
        LegacyMemberPayment(membership_type=self.full, payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="200", date=date(2011, 4, 20),
                      continues_membership=True).save()

        LegacyMemberPayment(membership_type=self.full, payment_type=BANK_PAYMENT,
                      member=jane, payment_value="200", date=date(2011, 3, 1),
                      continues_membership=False).save()
        LegacyMemberPayment(membership_type=self.full, payment_type=BANK_PAYMENT,
                      member=jane, payment_value="200", date=date(2011, 5, 10),
                      continues_membership=True).save()

        self.assertEqual(self.fred.membership_expiry_date(), jane.membership_expiry_date())
        self.assertEqual(self.fred.membership_expiry_date(), date(2011, 7, 29))

    def test_free_membership(self):
        """
        Free membership should count as if it was a payment
        """
        LegacyMemberPayment(membership_type=self.full, payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="200", date=date(2011, 3, 1),
                      continues_membership=False).save()
        LegacyMemberPayment(membership_type=self.full, payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="0", date=date(2011, 4, 1), free_months=2,
                      continues_membership=True).save()
        self.assertEqual(self.fred.membership_expiry_date(), date(2011, 6, 30))

    def test_mid_term_upgrade(self):
        """
        It should be possible to up/downgrade membership type midstream
        and have the expiry date change appropriately
        """
        # $240 buys 6 months associate (to Feb 2012)
        LegacyMemberPayment(membership_type=self.associate, payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="240", date=date(2011, 8, 1),
                      continues_membership=False).save()

        # After 1 month, we upgrade. The $200 left is 5 month associate or 4 month full
        LegacyMemberPayment(membership_type=self.full, payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="0", date=date(2011, 9, 1),
                      is_existing_upgrade=True).save()
        self.assertEqual(self.fred.member_type(date(2011, 11, 1)), self.full)
        self.assertEqual(self.fred.membership_expiry_date(), date(2011, 12, 30))

    def test_mid_term_upgrade_with_payment(self):
        """
        It's also possible to up/downgrade membership midstream with a payment
        at the same time
        """
        # $240 buys 6 months associate (to Feb 2012)
        LegacyMemberPayment(membership_type=self.associate, payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="240", date=date(2011, 8, 1),
                      continues_membership=False).save()

        # After 1 month, we upgrade. The $200 left is 5 month associate or 4 month full
        # but we also a pay in $100 for 2 more months of full
        LegacyMemberPayment(membership_type=self.full, payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="100", date=date(2011, 9, 1),
                      is_existing_upgrade=True).save()
        self.assertEqual(self.fred.member_type(date(2011, 2, 1)), self.full)
        self.assertEqual(self.fred.membership_expiry_date(), date(2012, 2, 29))
