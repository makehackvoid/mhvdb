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



class RecurringExpenseTest(TestCase):

    """
    Test cases for membership expiries
    """
    def setUp(self):
        self.fred = dummy_member("Fred Durst")
        self.fred.save()

    def assertPeriod(self, expense, fromdate, todate, dates):
        forperiod = expense.expenses_for_period(fromdate, todate)
        self.assertEqual([p.date for p in forperiod], dates)

    def testYearly(self):
        expense = RecurringExpense(description="Yearly payment of doom",
                                   date=date(2011,1,1),
                                   payment_type=CASH_PAYMENT,
                                   period_unit="Year",
                                   period=1)

        self.assertPeriod(expense, date(2011,1,1), date(2011,10,1), 
                          [ date(2011,1,1) ])

        self.assertPeriod(expense, date(1995,1,1), date(2014,2,1),
                          [ date(2011,1,1), date(2012,1,1), date(2013,1,1),
                            date(2014,1,1) ])

        expense.end_date = date(2012,2,1)
        self.assertPeriod(expense, date(1995,1,1), date(2014,2,1),
                          [ date(2011,1,1), date(2012,1,1) ])

    def testMonthly(self):
        expense = RecurringExpense(description="Monthly doom dose",
                                   date=date(2012,2,1),
                                   payment_type=BANK_PAYMENT,
                                   period_unit="Month",
                                   period=1)
        self.assertPeriod(expense, date(2012,1,1), date(2012,4,5),
                          [ date(2012,2,1), date(2012,3,1), date(2012,4,1) ])

        self.assertPeriod(expense, date(1995,1,1), date(2011,1,1), [])

        expense.end_date = date(2012,4,1)
        self.assertPeriod(expense, date(1995,1,1), date(2014,2,1),
                         [ date(2012,2,1), date(2012,3,1), date(2012,4,1) ])

    def testQuarterly(self):
        expense = RecurringExpense(description="Quarterly anti-doom insurance",
                                   date=date(2012,2,1),
                                   payment_type=BANK_PAYMENT,
                                   period_unit="Month",
                                   period=3)
        self.assertPeriod(expense, date(2012,1,1), date(2013,1,1),
                          [ date(2012,2,1), date(2012,5,1), date(2012,8,1),
                            date(2012,11,1) ])

        expense.end_date = date(2012,3,1)
        self.assertPeriod(expense, date(2012,1,1), date(2013,1,1),
                          [ date(2012,2,1) ])

    def testWeekly(self):
        expense = RecurringExpense(description="Weekly cola supply",
                                   date=date(2011,11,5), # Sat
                                   payment_type=BANK_PAYMENT,
                                   period_unit="Day",
                                   period=7)
        self.assertPeriod(expense, date(2012,1,1), date(2012,3,1),
                          [ date(2012,1,7), date(2012,1,14), # all saturdays
                            date(2012,1,21), date(2012,1,28), date(2012,2,4),
                            date(2012,2,11), date(2012,2,18), date(2012,2,25) ])

    def testLastDayOfMonth(self):
        """ A monthly payment should adjust around short months """
        expense = RecurringExpense(description="Last day of month tax",
                                   date=date(2012,1,31),
                                   payment_type=BANK_PAYMENT,
                                   period_unit="Month",
                                   period=1)
        self.assertPeriod(expense, date(2012,1,1), date(2012,5,1),
                          [ date(2012,1,31), date(2012,2,29), date(2012,3,31),
                            date(2012,4,30) ])


class TestBalanceSheetFunctions(TestCase):
    def testCombiningExpenses(self):
        RecurringExpense(description="Last day of month tax",
                         date=date(2012,1,31),
                         payment_type=BANK_PAYMENT,
                         payment_value=66,
                         period_unit="Month",
                         period=1).save()
        RecurringExpense(description="Annual filing cost",
                         date=date(2012,7,1),
                         payment_type=CASH_PAYMENT,
                         payment_value=150,
                         period_unit="Year",
                         period=1).save()
        Expense(description="Cheese",
                date=date(2012,6,5),
                payment_type=BANK_PAYMENT,
                payment_value=3.30).save()
        Expense(description="Crackers",
                date=date(2012,4,5),
                payment_type=BANK_PAYMENT,
                payment_value=2.50).save()

        allexpenses = Expense.objects.all_expenses_for_period( date(2012,3,1), date(2012,8,1) )
        self.assertEqual([(e.date,float(e.payment_value)) for e in allexpenses],
                         [ (date(2012,3,31), 66), # tax
                           (date(2012,4,5) , 2.50), # crackers
                           (date(2012,4,30), 66), # tax
                           (date(2012,5,31), 66), # tax
                           (date(2012,6,5), 3.30), # cheese
                           (date(2012,6,30), 66), # tax
                           (date(2012,7,1), 150), # filing cost
                           (date(2012,7,31), 66), # tax
                           ])

