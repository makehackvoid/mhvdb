from datetime import date
from datetime import datetime

from django.shortcuts import *

from finance.models import *

from core.decorators import auth_required

# from django.views.generic.simple import direct_to_template
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def _parse_date(string, default):
    """ should probably be using Django Forms for all this """
    try:
        return datetime.strptime(string, "%Y-%m-%d").date()
    except ValueError:
        return default

@auth_required
def balance(request):
    """
    Display a balance sheet
    """
    navitem = 'finance'

    date_from = _parse_date(request.GET.get("from", ""), date(2010,12,1))
    date_to = _parse_date(request.GET.get("to", ""), date.today())

    expenses = list(Expense.objects.all_expenses_for_period(date_from, date_to))
    income_items = list(Income.objects.filter(date__gte=date_from, date__lte=date_to))
    memberpayments = list(MemberPayment.objects.filter(date__gte=date_from, date__lte=date_to))
    legacymemberpayments = list(LegacyMemberPayment.objects.filter(date__gte=date_from, date__lte=date_to))
    expiringmemberpayments = list(ExpiringMemberPayment.objects.filter(date__gte=date_from, date__lte=date_to))

    income = sum(p.payment_value for p in memberpayments + legacymemberpayments + income_items)
    expense = sum(e.payment_value for e in expenses)

    period_balance = income - expense
    start_balance = Expense.objects.balance_at_date(date_from)
    end_balance = period_balance + start_balance

    items = sorted(expenses + memberpayments + income_items + legacymemberpayments + expiringmemberpayments, key=lambda e:e.date)

    return render_to_response('balance.html', locals())

def financial_reports(request):
    navitem = 'finance'
    years = range(2010, date.today().year+1);
    return render_to_response('financial_reports.html', locals())

@auth_required
def financial_report(request, year):
    """
    Display something approximating an end of financial year report
    """
    year = int(year)


    date_from = min(date(year,7,1), datetime.now().date())
    date_to = min(date(year+1,6,30), datetime.now().date())

    # income
    income_items = list(Income.objects.filter(date__gte=date_from, date__lte=date_to))
    income_by_category = {}
    for category in set(p.category for p in income_items):
        income_by_category[category] = sum(i.payment_value for i in income_items if i.category == category)
    income_by_category["Membership Payments"]  = sum(i.payment_value for i in MemberPayment.objects.filter(date__gte=date_from, date__lte=date_to))
    income_by_category["Membership Payments"] += sum(i.payment_value for i in LegacyMemberPayment.objects.filter(date__gte=date_from, date__lte=date_to))
    income_by_category["Membership Payments"] += sum(i.payment_value for i in ExpiringMemberPayment.objects.filter(date__gte=date_from, date__lte=date_to))

    income_total = sum(i for i in ( l for l in income_by_category.values() ))

    # expenses
    expense_items = list(Expense.objects.all_expenses_for_period(date_from, date_to))
    expense_by_category = {}
    for category in set(e.category for e in expense_items):
        expense_by_category[category] = sum(e.payment_value for e in expense_items if e.category == category)
    expense_total = sum(e.payment_value for e in expense_items)

    return render_to_response('financial_report.html', locals())