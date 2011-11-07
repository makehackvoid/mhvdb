from members.models import *
from django.contrib import admin

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

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('member', 'membership_type', 'date', 'duration')
admin.site.register(MemberPayment, PaymentAdmin)

admin.site.register(Income)
admin.site.register(IncomeCategory)
admin.site.register(Expense)
admin.site.register(ExpenseCategory)
admin.site.register(RecurringExpense)

