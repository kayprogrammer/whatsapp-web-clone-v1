from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.db.models import Case, F, When, Q, CharField
import pytz

from . models import Message
from . emojis import emojis
import json

User = get_user_model()

class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # request.session.flush()

        user = request.user
        
        messages = Message.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).select_related('sender', 'receiver')
        
        inbox_list = messages.annotate(
            other=Case(When(sender=user, then=F('receiver')), default=F('sender'), output_field=CharField())
        ).order_by('other', '-created_at').distinct('other')
        sorted_inbox_list = sorted(inbox_list, key=lambda x: x.created_at, reverse=True)
        
        all_users = User.objects.filter(is_email_verified=True, is_phone_verified=True, is_active=True).exclude(id=user.id).order_by('name')

        print(sorted_inbox_list)
        return render(request, 'chat/index.html', context={'inbox_list': sorted_inbox_list, 'messages': messages, 'all_users': all_users})

class ShowDirectMessagesView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = request.user
        try:    
            friend = User.objects.get(phone=data.get('phone'))
        except:
            return JsonResponse({'error': 'User not found'}) 

        recent_emojis = request.session.get('recent_emojis')
        messages = Message.objects.filter(Q(sender=user) | Q(receiver=user), Q(sender=friend) | Q(receiver=friend)).select_related('sender', 'receiver').order_by('created_at')
        messages.filter(sender=friend).update(is_read=True)
        response = dict()
        response['success'] = True
        response['html_data'] = render_to_string('chat/dm-page.html', {'messages': messages, 'friend': friend, 'recent_emojis': recent_emojis}, request=request)
        
        return JsonResponse(response)

class SendMessageView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = request.user
        message = data.get('message')
        try:
            friend = User.objects.get(phone=data.get('phone'))
        except:
            return JsonResponse({'error': 'User not found'}) 
        if len(message) < 1:
            return JsonResponse({'error': "You didn't type anything"})

        # Solve recent emojis
        recent_emojis = request.session.get('recent_emojis')
        em = []
        for i in message:
            if i in emojis:
                if recent_emojis and i in recent_emojis:
                    recent_emojis.remove(i)
                em.append(i)
            

        if len(em) > 0:
            em = list(set(em)) # remove duplicates
            if recent_emojis:
                updated_emojis = em + recent_emojis
                if len(updated_emojis) > 50:
                    n = len(updated_emojis) - 50
                    del updated_emojis[-n:]
                request.session['recent_emojis'] = updated_emojis
            else:
                updated_emojis = em
                if len(updated_emojis) > 50:
                    n = len(updated_emojis) - 50
                    del updated_emojis[-n:]
                request.session['recent_emojis'] = updated_emojis

        message_object = Message.objects.create(sender=user, receiver=friend, text=message)
        time = message_object.created_at.astimezone(pytz.timezone(request.user.tz.name))
        return JsonResponse({'success': True, 'message': message, 'time': time.strftime('%I:%M %p')})
