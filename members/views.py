from django.shortcuts import *
from members.models import *
from datetime import date

def members(request):
    """
    Display the list of members
    """
    members = Member.objects.all().order_by("last_name")
    sortby = { # is not possible to sort in the query as expiry/type are not DB fields
        'name'   : lambda m: ("%s %s" % (m.last_name, m.first_name)).lower(),
        'expiry' : lambda m: m.expiry_date(),
        'join'   : lambda m: m.join_date,
        'type'   : lambda m: m.member_type().membership_name
    }[request.GET.get('sort', 'name')]
    members = sorted(members, key=sortby)

    show_summary = True
    title = "Member Roster"
    # count how many of each member type we have
    alltypes = [ m.member_type().membership_name for m in members if m.member_type() is not None ]
    counts = sorted([(a, alltypes.count(a)) for a in set(alltypes)], key=lambda x:x[0])

    count = len(members)
    return render_to_response("members.html", locals())

def expiring_soon(request):
    """
    Display members expiring soon, in order of soonness
    """
    members = Member.objects.all().order_by("last_name")
    members = [ m for m in members if m.expiry_date() < date.today() + timedelta(days=30) ] # expired, or expiring soon
    members = reversed(sorted(members, key=lambda m: m.expiry_date()) )
    members = [ m for m in members if m.memberpayment_set.count() > 0 ] # hacky, this should be in DB layer

    show_summary = False
    title = "Expiring Members"
    return render_to_response("members.html", locals())


def _parse_date(string, default):
    """ should probably be using Django Forms for all this """
    try:
        return datetime.strptime(string, "%Y-%m-%d").date()
    except ValueError as e:
        return default

def balance(request):
    """
    Display a balance sheet
    """

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


def financial_report(request):
    """
    Display something approximating an end of financial year report
    """

    date_from = _parse_date(request.GET.get("from", ""), date(2010,7,1))
    date_to = _parse_date(request.GET.get("to", ""), date(2011,7,1))

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

def default(request):
    """
    Display a summary default page
    """

    lastexpense = Expense.objects.order_by("-date")[0]
    lastdonation = Income.objects.order_by("-date")[0]
    memberpayments = MemberPayment.objects.order_by("-date")[0]

    last_modified = max(lastexpense.date, lastdonation.date, memberpayments.date)
    return render_to_response("index.html", locals())


def emergency_contact(request, member_id):
    """
    Display emergency contact details
    """
    member = Member.objects.get(pk=member_id)
    return render_to_response("emergency_contact.html", locals())

