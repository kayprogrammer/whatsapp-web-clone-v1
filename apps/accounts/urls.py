from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # SIGNUP LOGIN LOGOUT
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),

    # EMAIL ACTIVATION AND PHONE VERIFICATION
    path('activate-user/<uidb64>/<token>', views.VerifyEmail.as_view(), name="activate"),
    path('verify-phone/', views.VerifyPhone.as_view(), name="verify-phone"),
    path('resend-activation-email/', views.ResendActivationEmail.as_view(), name="resend-activation-email"),
    path('resend-otp/', views.ResendOTP.as_view(), name="resend-otp"),

    # PASSWORD RESET
    path('reset-password/', views.CustomPasswordResetView.as_view(template_name="accounts/password-reset.html", html_email_template_name='accounts/password-reset-html-email.html'), name="reset_password"),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password-reset-sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(template_name="accounts/password-reset-form.html"), name="password_reset_confirm"),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password-reset-done.html"), name="password_reset_complete"),

]