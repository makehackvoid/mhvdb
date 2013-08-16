from django.conf.urls import *
from django.utils.functional import curry
from django.views.defaults import server_error, page_not_found

from django.contrib import admin
admin.autodiscover()

# Error handlers
handler500 = curry(server_error, template_name='../templates/admin/500.html')
handler404 = curry(page_not_found, template_name='../templates/admin/404.html')

urlpatterns = patterns('',
                       # Example:
                       # (r'^mhvdb/', include('mhvdb.foo.urls')),
                       # url(r'^$', 'mhvdb.views.home', name='home'),
                       (r'^members$', 'members.views.members'),
                       (r'^balance$', 'finance.views.balance'),
                       (r'^$',        'core.views.home'),
                       (r'^membercontact/(?P<member_id>\d+)/?$', 'members.views.emergency_contact'),
                       (r'^reports/?$',        'finance.views.financial_reports'),
                       (r'^reports/(?P<year>\d+)/?$',        'finance.views.financial_report'),
                       (r'^members/expiring$',        'members.views.expiring'),
                       (r'^members/expiring-access$',        'members.views.expiring_access'),
                       (r'^members/expiring-key$',        'members.views.expiring_key'),
                       (r'^members/expired$',        'members.views.expired'),
                       (r'^hadkey$',        'members.views.previous_full_member'),
                       (r'^signup$',        'members.views.signup'),
                       (r'^thanks$',      'members.views.signup_thankyou'),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       (r'^admin/', include(admin.site.urls)),

                       # reuse the admin login template
                       url(r'^login$', 'django.contrib.auth.views.login', {'template_name': '../templates/admin/login.html'}),
                       )
