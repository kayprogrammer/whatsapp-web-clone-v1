from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.db.models import Case, F, When, Q, CharField
from . models import Message

import json

User = get_user_model()

class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        
        messages = Message.objects.filter(Q(sender=user) | Q(receiver=user)).select_related('sender', 'receiver')

        inbox_list = messages.annotate(other=Case(When(sender=user, then=F('receiver')), default=F('sender'), output_field=CharField())).order_by('other', '-created_at').distinct('other')

        sorted_inbox_list = sorted(inbox_list, key=lambda x: x.created_at, reverse=True)
        return render(request, 'chat/index.html', context={'inbox_list': sorted_inbox_list, 'messages': messages})

class ShowDirectMessagesView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = request.user
        try:
            friend = User.objects.get(phone=data.get('phone'))
        except:
            return JsonResponse({'error': 'User not found'}) 

        messages = Message.objects.filter(Q(sender=user) | Q(receiver=user), Q(sender=friend) | Q(receiver=friend)).select_related('sender', 'receiver').order_by('created_at')
        messages.filter(sender=friend).update(is_read=True)
        response = dict()
        response['success'] = True
        response['html_data'] = render_to_string('chat/dm-page.html', {'messages': messages, 'friend': friend}, request=request)
        
        return JsonResponse(response)
