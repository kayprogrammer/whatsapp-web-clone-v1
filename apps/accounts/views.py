from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model

from . mixins import LogoutRequiredMixin
from . senders import Util, generate_token
from . forms import CustomUserCreationForm, PhoneVerificationForm

import sweetify

User = get_user_model()

class RegisterView(LogoutRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()

        context = {'form': form}
        return render(request, "accounts/register.html", context)

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Util.send_verification_email(request, user)
            return JsonResponse(
                {
                    'user': {'name': user.name, 'email': user.email, 'phone': user.phone},
                    'success': "Registration successful"
                }
            )
        else:
            print(form.errors.as_json())
            return JsonResponse({'errors': form.errors.as_json()})

class VerifyEmail(LogoutRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(kwargs.get('uidb64')))
            user = User.objects.get(id=uid)

        except Exception as e:
            user = None

        if user and generate_token.check_token(user, kwargs.get('token')):
            user.is_email_verified = True
            user.save()
            Util.send_sms_otp(user)
            return redirect(reverse('verify-phone'))

        return render(request, 'accounts/email-activation-failed.html', {"user": user})

class VerifyPhone(LogoutRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(phone=request.COOKIES.get('phone'))
            form = PhoneVerificationForm(request=request)
            if user.is_phone_verified:
                return redirect('/')
            return render(request, 'accounts/otp-verification.html', {'form':form})

        except:
            return redirect('/')

    def post(self, request, *args, **kwargs):
        form = PhoneVerificationForm(request.POST, request=request)
        if form.is_valid():
            return JsonResponse({'success': True})
        else:
            print(form.errors)
            return JsonResponse({'error': form.errors.as_json()})

class ResendActivationEmail(LogoutRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(phone=request.COOKIES.get('phone'))
            if user.is_email_verified:
                return JsonResponse({'email_verified': True})

            Util.send_verification_email(request, user)
            return JsonResponse({'success':True})
        except:
            return JsonResponse({"error": True})

class ResendOTP(LogoutRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(phone=request.COOKIES.get('phone'))
            if user.is_phone_verified:
                return JsonResponse({'phone_verified': True})
            Util.send_sms_otp(user)
            return JsonResponse({'success': True})
        except:
            return JsonResponse({"error": True})

class LoginView(LogoutRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "accounts/login.html")

    def post(self, request, *args, **kwargs):
        email_or_phone = request.POST.get('email_or_phone')
        password = request.POST.get('password')
        user = authenticate(request, username=email_or_phone, password=password)
        if not user:
            return JsonResponse({'credentials_error': 'Invalid credentials'})

        if not user.is_email_verified:
            Util.send_verification_email(request, user)
            return JsonResponse({'email_error': 'Email not verified. Check Email Again'})

        if not user.is_phone_verified:
            Util.send_sms_otp(user)
            return JsonResponse({'phone_error': 'Phone not verified. Check Phone Again'})

        login(request, user)
        return JsonResponse({'success': 'Login successful'})
