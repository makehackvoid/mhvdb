from datetime import date
from datetime import datetime

from django.shortcuts import *

from finance.models import *

# from django.views.generic.simple import direct_to_template
from django.conf import settings
import logging
from ipaddr import IPNetwork, IPAddress

logger = logging.getLogger(__name__)

def is_local_or_authenticated(request):
    """
    Return True if the user is authenticated, or is on a 'local' network
    as set under settings.LOCAL_IP_ADDRESSES
    """
    if request.user.is_authenticated():
        return True
    local_addrs = [ IPNetwork(addr) for addr in settings.LOCAL_IP_ADDRESSES ]
    try:
        remote = IPAddress(request.META["REMOTE_ADDR"])
        return any( remote in a for a in local_addrs )
    except:
        return False

def _parse_date(string, default):
    """ should probably be using Django Forms for all this """
    try:
        return datetime.strptime(string, "%Y-%m-%d").date()
    except ValueError:
        return default

def balance(request):
    """
    Display a balance sheet
    """
    navitem = 'finance'
    if not is_local_or_authenticated(request):
        return HttpResponseRedirect(settings.LOGIN_URL)

    date_from = _parse_date(request.GET.get("from", ""), date(2010,12,1))
    date_to = _parse_date(request.GET.get("to", ""), date.today())

    expenses = list(Expense.objects.all_expenses_for_period(date_from, date_to))
    income_items = list(Income.objects.filter(date__gte=date_from, date__lt=date_to))
    memberpayments = list(MemberPayment.objects.filter(date__gte=date_from, date__lt=date_to))

    income = sum(p.payment_value for p in memberpayments + income_items)
    expense = sum(e.payment_value for e in expenses)

    period_balance = income - expense
    start_balance = Expense.objects.balance_at_date(date_from)
    end_balance = period_balance + start_balance

    items = sorted(expenses + memberpayments + income_items, key=lambda e:e.date)

    return render_to_response('balance.html', locals())

def financial_reports(request):
    navitem = 'finance'
    years = range(2010, date.today().year+1);
    return render_to_response('financial_reports.html', locals())

def financial_report(request, year):
    """
    Display something approximating an end of financial year report
    """
    year = int(year)

    if not is_local_or_authenticated(request):
        return HttpResponseRedirect(settings.LOGIN_URL)

    date_from = min(date(year,7,1), datetime.now().date())
    date_to = min(date(year+1,7,1), datetime.now().date())

    # income
    income_items = list(Income.objects.filter(date__gte=date_from, date__lt=date_to))
    income_by_category = {}
    for category in set(p.category for p in income_items):
        income_by_category[category] = sum(i.payment_value for i in income_items if i.category == category)
    income_by_category["Membership Payments"] = sum(i.payment_value for i in MemberPayment.objects.filter(date__gte=date_from, date__lt=date_to))

    income_total = sum(i for i in ( l for l in income_by_category.values() ))

    # expenses
    expense_items = list(Expense.objects.all_expenses_for_period(date_from, date_to))
    expense_by_category = {}
    for category in set(e.category for e in expense_items):
        expense_by_category[category] = sum(e.payment_value for e in expense_items if e.category == category)
    expense_total = sum(e.payment_value for e in expense_items)

    return render_to_response('financial_report.html', locals())