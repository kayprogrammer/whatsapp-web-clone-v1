from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from . models import Timezone, User
from . validators import phone_regex_pattern

#-----ADMIN USER CREATION AND AUTHENTICATION------------#
class CustomAdminUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ["email", "name", "phone"]
        error_class = "error"


class CustomAdminUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["email", "name", "phone"]
        error_class = "error"

class MyAuthForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Invalid credentials. "
            "Fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }
    class Meta:
        model = User
        fields = ['username', 'password']
    def __init__(self, *args, **kwargs):
        super(MyAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Email or Phone number'
        self.fields['password'].label = 'Password'

#----------------------------------------------------------#

#-----GENERAL USER CREATION AND AUTHENTICATION-------------#
class CustomErrorMessages:
    email = {
        'unique': 'Email address already registered',
        'required': 'This field is required',
        'invalid': 'Enter a valid email address',
    }
    phone = {
        'unique': 'Phone number already registered',
        'required': 'This field is required',
    }
    tz = {
        'does_not_exist': 'Invalid timezone',
    }
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(error_messages=CustomErrorMessages.email, widget=forms.EmailInput(attrs={"placeholder": "Email Address", "class": "text email"}))
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Name", "class": "text"}))
    phone = forms.CharField(error_messages=CustomErrorMessages.phone, max_length=15, validators=[phone_regex_pattern], widget=forms.TextInput(attrs={"placeholder": "Phone Number", "class": "text email"}))
    tz = forms.ModelChoiceField(error_messages=CustomErrorMessages.tz, queryset=Timezone.objects.all())
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "text"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password", "class": "text w3lpass"}))
    terms_agreement = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "checkbox"}))

    class Meta:
        model = User
        fields = ["email", "name", "phone", "tz", "password1", "password2", "terms_agreement"]

#----------------------------------------------------------#

