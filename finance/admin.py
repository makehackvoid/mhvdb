from django.contrib import admin

from finance.models import *

class LegacyPaymentAdmin(admin.ModelAdmin):
    list_display = ('member', 'membership_type', 'date', 'duration', 'continues_membership')
admin.site.register(LegacyMemberPayment, LegacyPaymentAdmin)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'date', 'payment_value', 'category', 'via_member')
admin.site.register(Expense, ExpenseAdmin)

class IncomeAdmin(admin.ModelAdmin):
    list_display = ('description', 'date', 'payment_value', 'category')
admin.site.register(Income, IncomeAdmin)


admin.site.register(IncomeCategory)
admin.site.register(ExpenseCategory)
admin.site.register(RecurringExpense)
admin.site.register(MemberPayment)
admin.site.register(Product)
admin.site.register(ExpiringProduct)
admin.site.register(MembershipProduct)


