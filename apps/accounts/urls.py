from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    # SIGNUP LOGIN LOGOUT
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),

    # EMAIL ACTIVATION AND PHONE VERIFICATION
    path('verify-email/<uidb64>/<token>', views.VerifyEmail.as_view(), name="verify-email"),
    path('verify-phone/', views.VerifyPhone.as_view(), name="verify-phone"),
    path('resend-activation-email/', views.ResendActivationEmail.as_view(), name="resend-activation-email"),
    path('resend-otp/', views.ResendOTP.as_view(), name="resend-otp"),

    # PASSWORD RESET
    path('reset-password/', views.CustomPasswordResetView.as_view(template_name="accounts/password-reset.html", html_email_template_name='accounts/password-reset-html-email.html'), name="reset_password"),
    path('reset-password-sent/', views.CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(template_name="accounts/password-reset-form.html"), name="password_reset_confirm"),
    path('reset-password-complete/', views.CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),

]
