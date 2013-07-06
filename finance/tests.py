from django.test import TestCase

from finance.models import *

from decimal import Decimal


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


class RecurringExpenseTest(TestCase):
    """
    Test cases for membership expiries
    """

    def setUp(self):
        self.fred = dummy_member("Fred Durst")
        self.fred.save()

        self.doom = ExpenseCategory(name="doom")

    def assertPeriod(self, expense, fromdate, todate, dates):
        forperiod = expense.expenses_for_period(fromdate, todate)
        self.assertEqual([p.date for p in forperiod], dates)

    def testYearly(self):
        expense = RecurringExpense(description="Yearly payment of doom",
                                   date=date(2011, 1, 1),
                                   payment_type=CASH_PAYMENT,
                                   period_unit="Year",
                                   period=1, category=self.doom)

        self.assertPeriod(expense, date(2011, 1, 1), date(2011, 10, 1),
                          [date(2011, 1, 1)])

        self.assertPeriod(expense, date(1995, 1, 1), date(2014, 2, 1),
                          [date(2011, 1, 1), date(2012, 1, 1), date(2013, 1, 1),
                           date(2014, 1, 1)])

        expense.end_date = date(2012, 2, 1)
        self.assertPeriod(expense, date(1995, 1, 1), date(2014, 2, 1),
                          [date(2011, 1, 1), date(2012, 1, 1)])

    def testMonthly(self):
        expense = RecurringExpense(description="Monthly doom dose",
                                   date=date(2012, 2, 1),
                                   payment_type=BANK_PAYMENT,
                                   period_unit="Month",
                                   period=1, category=self.doom)
        self.assertPeriod(expense, date(2012, 1, 1), date(2012, 4, 5),
                          [date(2012, 2, 1), date(2012, 3, 1), date(2012, 4, 1)])

        self.assertPeriod(expense, date(1995, 1, 1), date(2011, 1, 1), [])

        expense.end_date = date(2012, 4, 1)
        self.assertPeriod(expense, date(1995, 1, 1), date(2014, 2, 1),
                          [date(2012, 2, 1), date(2012, 3, 1), date(2012, 4, 1)])

    def testQuarterly(self):
        expense = RecurringExpense(description="Quarterly anti-doom insurance",
                                   date=date(2012, 2, 1),
                                   payment_type=BANK_PAYMENT,
                                   period_unit="Month",
                                   period=3, category=self.doom)
        self.assertPeriod(expense, date(2012, 1, 1), date(2013, 1, 1),
                          [date(2012, 2, 1), date(2012, 5, 1), date(2012, 8, 1),
                           date(2012, 11, 1)])

        expense.end_date = date(2012, 3, 1)
        self.assertPeriod(expense, date(2012, 1, 1), date(2013, 1, 1),
                          [date(2012, 2, 1)])

    def testWeekly(self):
        expense = RecurringExpense(description="Weekly cola supply",
                                   date=date(2011, 11, 5),  # Sat
                                   payment_type=BANK_PAYMENT,
                                   period_unit="Day",
                                   period=7, category=self.doom)
        self.assertPeriod(expense, date(2012, 1, 1), date(2012, 3, 1),
                          [date(2012, 1, 7), date(2012, 1, 14),  # all saturdays
                           date(2012, 1, 21), date(2012, 1, 28), date(2012, 2, 4),
                           date(2012, 2, 11), date(2012, 2, 18), date(2012, 2, 25)])

    def testLastDayOfMonth(self):
        """ A monthly payment should adjust around short months """
        expense = RecurringExpense(description="Last day of month tax",
                                   date=date(2012, 1, 31),
                                   payment_type=BANK_PAYMENT,
                                   period_unit="Month",
                                   period=1, category=self.doom)
        self.assertPeriod(expense, date(2012, 1, 1), date(2012, 5, 1),
                          [date(2012, 1, 31), date(2012, 2, 29), date(2012, 3, 31),
                           date(2012, 4, 30)])


class TestBalanceSheetFunctions(TestCase):
    def testCombiningExpenses(self):
        tax = ExpenseCategory(name="Tax")
        tax.save()
        food = ExpenseCategory(name="Food")
        food.save()
        RecurringExpense(description="Last day of month tax",
                         date=date(2012, 1, 31),
                         payment_type=BANK_PAYMENT,
                         payment_value=66,
                         period_unit="Month",
                         category=tax,
                         period=1).save()
        RecurringExpense(description="Annual filing cost",
                         date=date(2012, 7, 1),
                         payment_type=CASH_PAYMENT,
                         payment_value=150,
                         period_unit="Year",
                         category=tax,
                         period=1).save()
        Expense(description="Cheese",
                date=date(2012, 6, 5),
                payment_type=BANK_PAYMENT,
                payment_value=Decimal("3.30"),
                category=food).save()
        Expense(description="Crackers",
                date=date(2012, 4, 5),
                payment_type=BANK_PAYMENT,
                payment_value=Decimal("2.50"),
                category=food).save()

        allexpenses = Expense.objects.all_expenses_for_period(date(2012, 3, 1), date(2012, 8, 1))
        self.assertEqual([(e.date, float(e.payment_value)) for e in allexpenses],
                         [(date(2012, 3, 31), 66),   # tax
                          (date(2012, 4, 5), 2.50),  # crackers
                          (date(2012, 4, 30), 66),   # tax
                          (date(2012, 5, 31), 66),   # tax
                          (date(2012, 6, 5), 3.30),  # cheese
                          (date(2012, 6, 30), 66),   # tax
                          (date(2012, 7, 1), 150),   # filing cost
                          (date(2012, 7, 31), 66),   # tax
                          ])
