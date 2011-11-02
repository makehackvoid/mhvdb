"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from members.models import *
from datetime import date

def dummy_member(name, join_date=date(2011,1,1)):
    """
    Utility function to make a dummy member
    """
    return Member(last_name=name.split(" ")[1],
                  first_name=name.split(" ")[0],
                  join_date=date(1995,1,1),
                  address="Test Lane",
                  emergency_contact_name="TestContact",
                  emergency_contact_number="5551234",
                  medical_info="Is a test case, DNR"
                  )

class MembershipExpiryTest(TestCase):
    """
    Test cases form embership expiries
    """
    def setUp(self):
        self.fred = dummy_member("Fred Durst")
        self.fred.save()

        # Membership type structure
        self.associate = Membership(membership_name="Associate")
        self.full = Membership(membership_name="Full")
        self.associate.save()
        self.full.save()

        # Dummy membership cost structure - associate went up 1 June 2011, full came down(!)
        MembershipCost(membership=self.associate, monthly_cost="20", valid_from=date(2011,1,1)).save()
        MembershipCost(membership=self.associate, monthly_cost="40", valid_from=date(2011,6,1)).save()
        MembershipCost(membership=self.full, monthly_cost="100", valid_from=date(2011,1,1)).save()
        MembershipCost(membership=self.full, monthly_cost="50", valid_from=date(2011,6,1)).save()

    def test_durations(self):
        """
        Test that the system knows what membership costs on various dates
        """
        self.assertEqual( MembershipCost.objects.applicable_cost(self.associate, date(2011,2,1)).monthly_cost, 20 )
        self.assertEqual( MembershipCost.objects.applicable_cost(self.associate, date(2011,7,1)).monthly_cost, 40 )
        self.assertEqual( MembershipCost.objects.applicable_cost(self.full, date(2012,1,1)).monthly_cost, 50 )


    def test_auto_duration(self):
        """
        If a new MemberPayment gets inserted, its duration (if empty) should automatically be 
        calculated based on the cost that applies at the time
        """
        payment = MemberPayment(membership_type=self.associate, payment_type=BANK_PAYMENT,
                                member=self.fred, payment_value="480", date=date(2011,8,1)) # $40/mo * 12 months
        payment.save()
        payment = self.fred.memberpayment_set.all()[0]
        self.assertEqual(payment.duration(), 12)
        self.assertEqual(self.fred.expiry_date(), date(2012,7,31))

    def test_renewal_before_expiry(self):
        """
        If a member renews before their membership expires, the expiry date should be added to the end
        of their existing membership period
        """
        MemberPayment(membership_type=self.associate,payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="120", date=date(2011,8,1)).save() # $40/mo * 3 months
        MemberPayment(membership_type=self.associate, payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="120", date=date(2011,10,1),
                      continues_membership=True).save() # 3 more months
        self.assertEqual(self.fred.expiry_date(), date(2012,1,30))

    def test_renewal_after_expiry(self):
        """
        If a member renews after their expiry date, but didn't stop their membership, the renewal
        payment should be backdated
        """
        MemberPayment(membership_type=self.associate,payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="120", date=date(2011,8,1)).save() # $40/mo * 3 months
        MemberPayment(membership_type=self.associate, payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="120", date=date(2011,12,1),
                      continues_membership=True).save() # 3 more months, LATE!
        self.assertEqual(self.fred.expiry_date(), date(2012,1,30))


    def test_break_in_membership(self):
        """
        If a member lapses back to casual, then starts again, then their new membership doesn't
        count back to the old one
        """
        MemberPayment(membership_type=self.associate,payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="120", date=date(2011,8,1)).save() # $40/mo * 3 months
        MemberPayment(membership_type=self.associate, payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="120", date=date(2012,8,1)).save() # 3 months again
        self.assertEqual(self.fred.expiry_date(), date(2012,10,31))



    def test_pro_rata_over_rate_reduction(self):
        """
        If the membership rate goes down during a membership, the membership
        should be pro rata extended to match the new value
        """

        # $200 buys 2 months on 1 May, but would buy 4 months on 1 June... so result
        # should be 3 months
        MemberPayment(membership_type=self.full,payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="200", date=date(2011,5,1)).save()
        self.assertEqual(self.fred.expiry_date(), date(2011,7,30))

    def test_no_pro_rate_over_rate_hike(self):
        """
        OTOH, if the membership rate goes up during a membership, it's a bit rich to ask
        for it to be pro rataed shorter - so we don't do that
        """

        # $120 buys 6 months on 1 May, and that's how it stays
        MemberPayment(membership_type=self.associate,payment_type=BANK_PAYMENT,
                      member=self.fred, payment_value="120", date=date(2011,5,1)).save()
        self.assertEqual(self.fred.expiry_date(), date(2011,10,30))

