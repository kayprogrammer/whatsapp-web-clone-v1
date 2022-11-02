from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
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
    class Meta:
        model = User
        fields = ['username', 'password']
    def __init__(self, *args, **kwargs):
        super(MyAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Email or Phone number'
        self.fields['password'].label = 'Password'

#----------------------------------------------------------#

#-----GENERAL USER CREATION AND AUTHENTICATION-------------#
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email Address", "class": "text email"}))
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Name", "class": "text"}))
    phone = forms.CharField(max_length=15, validators=[phone_regex_pattern], widget=forms.TextInput(attrs={"placeholder": "Phone Number", "class": "text email"}))
    tz = forms.ModelChoiceField(queryset=Timezone.objects.all())
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "text"}))
    password2 = forms.EmailField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password", "class": "text w3lpass"}))
    terms_agreement = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "checkbox"}))

    class Meta:
        model = User
        fields = ["email", "name", "phone", "tz", "password1", "password2", "terms_agreement"]

    def clean_password2(self):
        super(RegisterForm, self).clean()

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1 == password2:
            return forms.ValidationError('Password Mismatch')
        return password2
#----------------------------------------------------------#

