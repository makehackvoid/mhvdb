from ipaddr import IPNetwork, IPAddress
from functools import wraps
from django.conf import settings
from django.shortcuts import HttpResponseRedirect



def auth_required(func):
    """
    This is a decorator used to check whether a user is local or authenticated.
    If not it redirects the user to the login page.
    """

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

    def decorator(request, *args, **kwargs):        
        if not is_local_or_authenticated(request):
            return HttpResponseRedirect(settings.LOGIN_URL)
        else:
            return func(request, *args, **kwargs)
    return wraps(func)(decorator)