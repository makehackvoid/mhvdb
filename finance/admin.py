from django.contrib import admin
from django import forms

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

class MemberPaymentForm(forms.ModelForm):
    class Meta:
        model = MemberPayment
    def __init__(self, *args, **kwargs):
        super(MemberPaymentForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.exclude(id__in=ExpiringProduct.objects.all())
class MemberPaymentAdmin(admin.ModelAdmin):
    form = MemberPaymentForm
admin.site.register(MemberPayment, MemberPaymentAdmin)




admin.site.register(IncomeCategory)
admin.site.register(ExpenseCategory)
admin.site.register(RecurringExpense)
admin.site.register(Product)
admin.site.register(ExpiringProduct)
admin.site.register(MembershipProduct)
admin.site.register(ExpiringMemberPayment)


