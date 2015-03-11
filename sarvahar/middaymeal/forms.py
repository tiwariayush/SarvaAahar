from django import forms
from middaymeal.models import *

class LoginForm(forms.Form):

    name = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class SignUpForm(forms.ModelForm):

    name = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    district = forms.ChoiceField(required=False, choices=[(x.id, x.name) for x in District.objects.all()])
    block = forms.ChoiceField(required=False, choices=[(x.id, x.name) for x in Block.objects.all()])
    panchayat = forms.ChoiceField(required=False, choices=[(x.id, x.name) for x in Panchayat.objects.all()])
    village = forms.ChoiceField(required=False, choices=[(x.id, x.name) for x in Village.objects.all()])
    aanganwadi = forms.ChoiceField(required=False, choices=[(x.id, x.name) for x in Aanganwadi.objects.all()])

    class Meta:
        model = UserProfile
        exclude = ('user', 'category_data',)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password', '')
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError("The two password fields didn't match")
        return confirm_password

class ChildEntryForm(forms.ModelForm):

    class Meta:
        model = Child

class ChildConditionForm(forms.ModelForm):

    class Meta:
        model = ChildConditions
        exclude = ('child', 'age', 'body_mass_index')
