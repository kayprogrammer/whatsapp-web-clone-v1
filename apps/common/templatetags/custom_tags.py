from django import template
from django.utils import timezone
import pytz

register = template.Library()

@register.filter
def sweet_timestamp(date, local_tz):
    # Get current local time of user and date object in local time
    current_date = timezone.now().astimezone(pytz.timezone(local_tz)) 
    date_obj = date.astimezone(pytz.timezone(local_tz))

    new_dt = date_obj
    if current_date.date() == date_obj.date():
        new_dt = date_obj.strftime('%H:%M')
    elif current_date.day - date_obj.day == 1 and current_date.month == date_obj.month and current_date.year == date_obj.year:
        new_dt = 'yesterday'
    else:
        new_dt = date_obj.strftime('%d/%m/%Y')
    return new_dt

@register.filter
def dm_sweet_timestamp(date, local_tz):
    # Get current local time of user and date object in local time
    current_date = timezone.now().astimezone(pytz.timezone(local_tz)) 
    date_obj = date.astimezone(pytz.timezone(local_tz))

    new_dt = date_obj
    if current_date.date() == date_obj.date():
        new_dt = 'Today'
    elif current_date.day - date_obj.day == 1 and current_date.month == date_obj.month and current_date.year == date_obj.year:
        new_dt = 'Yesterday'
    else:
        new_dt = date_obj.strftime('%d/%m/%Y')
    return new_dt

@register.filter
def unread_messages_count(messages, other_user):
    count = messages.filter(sender=other_user, is_read=False).select_related('sender', 'receiver').count()
    return count
