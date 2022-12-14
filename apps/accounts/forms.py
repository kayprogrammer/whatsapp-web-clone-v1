from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

from . senders import Util, MessageThread
from . models import Timezone, User, Otp
from . validators import phone_regex_pattern

User = get_user_model()

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
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Name", "class": "text"}))
    email = forms.EmailField(error_messages=CustomErrorMessages.email, widget=forms.EmailInput(attrs={"placeholder": "Email Address", "class": "text email"}))
    phone = forms.CharField(error_messages=CustomErrorMessages.phone, max_length=15, validators=[phone_regex_pattern], widget=forms.TextInput(attrs={"placeholder": "Phone Number", "class": "text email"}))
    tz = forms.ModelChoiceField(error_messages=CustomErrorMessages.tz, queryset=Timezone.objects.all())
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "text"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password", "class": "text w3lpass"}))
    terms_agreement = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "checkbox"}))

    class Meta:
        model = User
        fields = ["name", "email", "phone", "tz", "password1", "password2", "terms_agreement"]

#----------------------------------------------------------#

class PhoneVerificationForm(forms.Form):
    otp = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder": "Enter Otp"}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.phone = kwargs.pop('phone', None)
        self.user = kwargs.pop('user', None)

        super(PhoneVerificationForm, self).__init__(*args, **kwargs)

    def clean_otp(self):
        request = self.request
        user = self.user
        otp = self.cleaned_data.get('otp')
        
        otp_object = Otp.objects.filter(user=user, value=otp)
        if not otp_object.exists():
            raise ValidationError('Invalid Otp', code="invalid_otp")
        otp_object = otp_object.get()
        diff = timezone.now() - otp_object.updated_at
        if diff.total_seconds() > 900:
            raise ValidationError('Expired Otp', code="expired_otp") 

        user.is_phone_verified = True
        user.save()
        Util.send_welcome_email(request, user)
        return otp

class CustomPasswordResetForm(PasswordResetForm):
    # Taken from django.contrib.auth.forms
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "Email Address"}),
    )

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        MessageThread(email_message).start()

class CustomSetPasswordForm(SetPasswordForm):
    # Taken from django.contrib.auth.forms
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "placeholder": "New Password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "placeholder": "Repeat New Password"}),
    )