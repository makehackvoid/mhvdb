from django.conf.urls import *
from django.utils.functional import curry
from django.views.defaults import server_error, page_not_found

from django.contrib import admin
admin.autodiscover()

# Error handlers
handler500 = curry(server_error, template_name='admin/500.html')
handler404 = curry(page_not_found, template_name='admin/404.html')

urlpatterns = patterns('',
                       # Example:
                       # (r'^mhvdb/', include('mhvdb.foo.urls')),
                       # url(r'^$', 'mhvdb.views.home', name='home'),
                       (r'^members$', 'members.views.members'),
                       (r'^balance$', 'members.views.balance'),
                       (r'^$',        'members.views.default'),
                       (r'^membercontact/(?P<member_id>\d+)/?$', 'members.views.emergency_contact'),
                       (r'^report$',        'members.views.financial_report'),
                       (r'^expiring$',        'members.views.expiring_soon'),
                       (r'^signup$',        'members.views.signup'),
                       (r'^thanks$',      'members.views.signup_thankyou'),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       (r'^admin/', include(admin.site.urls)),

                       # reuse the admin login template
                       url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
                       )
