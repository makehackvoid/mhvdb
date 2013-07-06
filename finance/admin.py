from django.contrib import admin

from finance.models import *

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('member', 'membership_type', 'date', 'duration', 'continues_membership')
admin.site.register(MemberPayment, PaymentAdmin)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'date', 'payment_value', 'category', 'via_member')
admin.site.register(Expense, ExpenseAdmin)

class IncomeAdmin(admin.ModelAdmin):
    list_display = ('description', 'date', 'payment_value', 'category')
admin.site.register(Income, IncomeAdmin)


admin.site.register(IncomeCategory)
admin.site.register(ExpenseCategory)
admin.site.register(RecurringExpense)

