from . import views
from django.urls import path


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
]