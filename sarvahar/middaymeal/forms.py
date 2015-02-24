from django import forms
from middaymeal.models import *

class LoginForm(forms.ModelForm):
    name = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = UserProfile
        widget = {
                'password': forms.PasswordInput(),
            }
        exclude = ('user',)

class ChildEntryForm(forms.ModelForm):

    class Meta:
        model = Child

class ChildConditionForm(forms.ModelForm):

    class Meta:
        model = ChildConditions
        exclude = ('child',)
