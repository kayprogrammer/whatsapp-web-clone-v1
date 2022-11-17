from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('chat/show-direct-messages/', views.ShowDirectMessagesView.as_view(), name="show-dm"),
    path('chat/send-message/', views.SendMessageView.as_view(), name="send-message")
]