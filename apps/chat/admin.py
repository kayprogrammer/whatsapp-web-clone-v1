from django.contrib import admin
from . models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'is_read', 'created_at']
    list_filter = ['sender', 'receiver', 'is_read', 'created_at']
    list_display_links = ['sender', 'receiver', ]

admin.site.register(Message, MessageAdmin)
