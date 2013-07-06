from django.contrib import admin

from members.models import *
from finance.models import MemberPayment


class PhoneInline(admin.StackedInline):
    model = Phone
    extra = 1

class EmailInline(admin.StackedInline):
    model = Email
    extra = 1

class PaymentInline(admin.TabularInline):
    model=MemberPayment
    extra=0

class MemberAdmin(admin.ModelAdmin):
#    fieldsets = [
#        (None,               {'fields': ['question']}),
#        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#    ]
    list_display = ('fullname', 'join_date', 'member_type', 'expiry_date' )
    inlines = [PhoneInline, EmailInline, PaymentInline ]

admin.site.register(Member, MemberAdmin)

class MembershipCostInline(admin.TabularInline):
    model = MembershipCost
    extra = 1

class MembershipAdmin(admin.ModelAdmin):
    inlines = [ MembershipCostInline ]
admin.site.register(Membership, MembershipAdmin)
