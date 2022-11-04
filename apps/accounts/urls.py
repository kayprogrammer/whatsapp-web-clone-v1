from . import views
from django.urls import path


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),

    path('activate-user/<uidb64>/<token>', views.VerifyEmail.as_view(), name="activate"),
    path('verify-phone/', views.VerifyPhone.as_view(), name="verify-phone"),
    path('resend-activation-email/', views.ResendActivationEmail.as_view(), name="resend-activation-email"),
    path('resend-otp/', views.ResendOTP.as_view(), name="resend-otp"),

]