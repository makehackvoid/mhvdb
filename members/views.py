import csv
from django.http import HttpResponse

from datetime import date
from datetime import datetime

from django.core.urlresolvers import reverse
from django.shortcuts import *
from django.template import RequestContext

from members.models import *

from core.decorators import auth_required

from forms import *

# from django.views.generic.simple import direct_to_template
from django.conf import settings
import logging


logger = logging.getLogger(__name__)


@auth_required
def members(request):
    """
    Display the list of members
    """
    navitem = 'members'

    members = Member.objects.all().order_by("last_name")
    sortby = { # is not possible to sort in the query as expiry/type are not DB fields
        'name'   : lambda m: ("%s %s" % (m.last_name, m.first_name)).lower(),
        'expiry' : lambda m: m.membership_expiry_date(),
        'join'   : lambda m: m.join_date,
        'type'   : lambda m: m.member_type().membership_name
    }[request.GET.get('sort', 'name')]
    members = filter(lambda x: x.member_type().membership_name != settings.DEFAULT_MEMBERSHIP_NAME, members)
    members = sorted(members, key=sortby)


    show_summary = True
    # count how many of each member type we have
    alltypes = [m.member_type() for m in members]
    counts = sorted([(a, alltypes.count(a)) for a in set(alltypes)], key=lambda x: x[0])

    count = len(members)
    return render_to_response("members.html", locals())

@auth_required
def members_csv(request):
    """
    Export members as csv file
    """
    navitem = 'members'

    members = Member.objects.all().order_by("last_name")
    sortby = { # is not possible to sort in the query as expiry/type are not DB fields
        'name'   : lambda m: ("%s %s" % (m.last_name, m.first_name)).lower(),
        'expiry' : lambda m: m.membership_expiry_date(),
        'join'   : lambda m: m.join_date,
        'type'   : lambda m: m.member_type().membership_name
    }[request.GET.get('sort', 'name')]
    # members = filter(lambda x: x.member_type().membership_name != settings.DEFAULT_MEMBERSHIP_NAME, members)
    members = sorted(members, key=sortby)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mhvdb_members.csv"'

    writer = csv.writer(response)
    writer.writerow(['fullname', 'membership_expiry_date', 'join_date', 'key_expiry_date', 'member_id', 'phone', 'member_email'])
    for m in members:
        writer.writerow([m.fullname(), m.membership_expiry_date(), m.join_date, m.key_expiry_date(), m.id, m.member_phone(), m.member_email()])
    return response

@auth_required
def expiring(request):
    """
    Display members expiring soon, in order of soonness
    """
    navitem = 'members'

    members = Member.objects.all().order_by("last_name")
    members = [ m for m in members if m.membership_expiry_date() is not None and m.membership_expiry_date() < date.today() + timedelta(days=30) and m.membership_expiry_date() > date.today() - timedelta(days=60)] # expired, or expiring soon
    members = reversed(sorted(members, key=lambda m: m.membership_expiry_date()) )
    expiry_type = "Expiring Members"
    return render_to_response("expiring.html", locals())

@auth_required
def expiring_key(request):
    """
    Display members with keys expiring soon, in order of soonness
    """
    navitem = 'members'

    members = Member.objects.all().order_by("last_name")
    members = [ m for m in members if m.key_expiry_date() is not None and m.key_expiry_date() < date.today() + timedelta(days=30) and m.key_expiry_date() > date.today() - timedelta(days=60)] # expired, or expiring soon
    members = reversed(sorted(members, key=lambda m: m.key_expiry_date()) )
    expiry_type = "Members with expiring keys"
    return render_to_response("expiring.html", locals())

@auth_required
def expiring_access(request):
    """
    Display members with access expiring soon, in order of soonness
    """
    navitem = 'members'

    members = Member.objects.all().order_by("last_name")
    members = [ m for m in members if m.access_expiry_date() is not None and m.access_expiry_date() < date.today() + timedelta(days=30) and m.access_expiry_date() > date.today() - timedelta(days=60)] # expired, or expiring soon
    members = reversed(sorted(members, key=lambda m: m.access_expiry_date()) )
    expiry_type = "Members with expiring monthly access"
    return render_to_response("expiring.html", locals())

@auth_required
def expired(request):
    """
    Display expired members, in order of soonness
    """
    navitem = 'members'

    members = Member.objects.all().order_by("last_name")
    members = [ m for m in members if m.membership_expiry_date() is not None and m.membership_expiry_date() < date.today()]
    sorted(members, key=lambda m: m.membership_expiry_date()).reverse()

    count = len(members)

    return render_to_response("expired.html", locals())

@auth_required
def previous_full_member(request):
    """
    Display everyone who has been full member (looking for keys)
    """
    navitem = 'members'

    members = Member.objects.all().order_by("last_name")
    members = [m for m in members if m.was_full_member()]
    members = reversed(sorted(members, key=lambda m: m.membership_expiry_date()) )

    show_summary = False
    title = "Previous Full Members"
    return render_to_response("members.html", locals())

def _parse_date(string, default):
    """ should probably be using Django Forms for all this """
    try:
        return datetime.strptime(string, "%Y-%m-%d").date()
    except ValueError:
        return default

@auth_required
def emergency_contact(request, member_id):
    """
    Display emergency contact details
    """
    navitem = 'members'

    member = Member.objects.get(pk=member_id)
    return render_to_response("emergency_contact.html", locals())


def signup(request):
    """
    Display/process a signup form
    """
    navitem = 'members'
    if request.method == 'POST':
        form = MemberSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(signup_thankyou))
    else:
        form = MemberSignupForm()
    return render_to_response('signup.html', locals(), context_instance=RequestContext(request))

def signup_thankyou(request):
    return render_to_response("thanks.html", locals())
