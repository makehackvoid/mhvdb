from django.contrib import admin

from members.models import *
from finance.models import LegacyMemberPayment, ExpiringMemberPayment


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

class LegacyMembershipCostInline(admin.TabularInline):
    model = LegacyMembershipCost
    extra = 0

class LegacyMembershipAdmin(admin.ModelAdmin):
    inlines = [ LegacyMembershipCostInline ]
admin.site.register(LegacyMembership, LegacyMembershipAdmin)

# starting to add expiring payments (not working)
# class ExpiringMemberPaymentInline(admin.TabularInline):
#     model = ExpiringMemberPayment
#     extra = 0

# class ExpiringMemberPaymentAdmin(admin.ModelAdmin):
#     inlines = [ ExpiringMemberPaymentInline ]
# admin.site.register(ExpiringMemberPaymentAdmin)

admin.site.register(Membership)
