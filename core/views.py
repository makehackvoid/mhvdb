# Create your views here.
from django.shortcuts import *

from finance.models import *


def home(request):
    """
    Display a summary default page
    """
    navitem = 'home'
    lastexpense = Expense.objects.order_by("-date")[0]
    lastdonation = Income.objects.order_by("-date")[0]
    memberpayments = LegacyMemberPayment.objects.order_by("-date")[0]

    last_modified = max(lastexpense.date, lastdonation.date, memberpayments.date)
    return render_to_response("index.html", locals())