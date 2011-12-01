from django.forms import ModelForm
import django.forms as forms
from django.forms.models import inlineformset_factory
from models import *

class MemberSignupForm(ModelForm):
    class Meta:
        model = Member
        fields = ( 'first_name', 'last_name', 'phone_number', 'email_address', 'address', 'username',
                   'emergency_contact_name', 'emergency_contact_number', 'medical_info' )
        exclude = ( 'join_date' )

    phone_number = forms.CharField(max_length=12, label="Phone Number")
    email_address = forms.CharField(max_length=50, label="Email Address")

    def save(self):
        if self.instance.join_date is None:
            self.instance.join_date = date.today()
        member = super(MemberSignupForm, self).save()
        member.save()
        phone = Phone(member=member, phone_number=self.cleaned_data["phone_number"])
        email = Email(member=member, email=self.cleaned_data["email_address"])
        phone.save()
        email.save()
