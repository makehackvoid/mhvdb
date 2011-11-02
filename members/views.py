from django.template import Context, loader
from django.http import HttpResponse
from members.models import *

def members(request):
    """
    Display the list of members
    """
    membership = Member.objects.all().order_by("last_name")
    sortby = { # is not possible to sort in the query as expiry/type are not DB fields
        'name'   : lambda m: ("%s %s" % (m.last_name, m.first_name)).lower(),
        'expiry' : lambda m: m.expiry_date(),
        'join'   : lambda m: m.join_date,
        'type'   : lambda m: m.member_type().membership_name
    }[request.GET.get('sort', 'name')]
    membership = sorted(membership, key=sortby)

    # count how many of each member type we have
    alltypes = [ m.member_type().membership_name for m in membership ]
    counts = sorted([(a, alltypes.count(a)) for a in set(alltypes)], key=lambda x:x[0])

    t = loader.get_template('members.html')
    c = Context({
        'members': membership,
        'count' : len(membership),
        'counts' : counts,
    })
    return HttpResponse(t.render(c))
