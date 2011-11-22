from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^mhvdb/', include('mhvdb.foo.urls')),
    (r'^members$', 'members.views.members'),
    (r'^balance$', 'members.views.balance'),
    (r'^$',        'members.views.default'),
    (r'^membercontact/(?P<member_id>\d+)/?$', 'members.views.emergency_contact'),
    (r'^report$',        'members.views.financial_report'),
    (r'^expiring$',        'members.views.expiring_soon'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
