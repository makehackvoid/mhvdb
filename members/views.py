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

    # count how many of each member type we have
    alltypes = [ m.member_type().membership_name for m in members if m.member_type() is not None ]
    counts = sorted([(a, alltypes.count(a)) for a in set(alltypes)], key=lambda x:x[0])

    count = len(members)
    return render_to_response("members.html", locals())


def balance(request):
    """
    Display a balance sheet
    """

    date_from=date(2010,1,1)  # TODO: use a form to choose these!
    date_to=date.today()

    expenses = list(Expense.objects.all_expenses_for_period(date_from, date_to))
    donations = list(Donation.objects.filter(date__gte=date_from, date__lt=date_to))
    memberpayments = list(MemberPayment.objects.filter(date__gte=date_from, date__lt=date_to))

    income = sum(p.payment_value for p in memberpayments + donations)
    expense = sum(e.payment_value for e in expenses)
    balance = income - expense

    items = sorted(expenses + memberpayments + donations, key=lambda e:e.date)

    return render_to_response('balance.html', locals())


def default(request):
    """
    Display a summary default page
    """

    lastexpense = Expense.objects.order_by("-date")[0]
    lastdonation = Donation.objects.order_by("-date")[0]
    memberpayments = MemberPayment.objects.order_by("-date")[0]

    last_modified = max(lastexpense.date, lastdonation.date, memberpayments.date)
    return render_to_response("index.html", locals())
