from django.contrib import admin

from members.models import *
from finance.models import LegacyMemberPayment


class PhoneInline(admin.StackedInline):
    model = Phone
    extra = 0

class EmailInline(admin.StackedInline):
    model = Email
    extra = 0

class PaymentInline(admin.TabularInline):
    model=LegacyMemberPayment
    extra=0

class MemberAdmin(admin.ModelAdmin):
#    fieldsets = [
#        (None,               {'fields': ['question']}),
#        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#    ]
    list_display = ('fullname', 'join_date', 'member_type', 'membership_expiry_date', 'access_expiry_date', 'key_expiry_date' )
    inlines = [PhoneInline, EmailInline, PaymentInline ]

admin.site.register(Member, MemberAdmin)

class MembershipCostInline(admin.TabularInline):
    model = LegacyMembershipCost
    extra = 0

class MembershipAdmin(admin.ModelAdmin):
    inlines = [ MembershipCostInline ]
admin.site.register(LegacyMembership, MembershipAdmin)

admin.site.register(Membership)
