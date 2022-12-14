from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string 
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

from sms import Message
import six
import threading
import random

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.id)+six.text_type(timestamp)+six.text_type(user.is_email_verified))

email_verification_generate_token = EmailVerificationTokenGenerator()

class MessageThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

class Util:
    @staticmethod
    def send_verification_email(request, user):
        current_site = f'{request.scheme}://{request.get_host()}'
        subject = 'Activate your account'
        message = render_to_string('accounts/email-activation-message.html', {
            'name':user.name, 
            'domain':current_site, 
            'site_name': settings.SITE_NAME,
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'token': email_verification_generate_token.make_token(user),
            'user_id': user.id
        })

        email_message = EmailMessage(subject=subject, body=message, to=[user.email])
        email_message.content_subtype = "html"
        
        MessageThread(email_message).start()
    
    @staticmethod
    def send_sms_otp(user):
        code = random.randint(100000, 999999)
        from . models import Otp 
        otp, created = Otp.objects.get_or_create(user=user)
        otp.value = code
        otp.save()
        message = Message(
            f'Hello {user.name}! \nYour Phone Verification OTP from {settings.SITE_NAME} is {code} \nExpires in 15 minutes',
            settings.DEFAULT_FROM_PHONE,
            [user.phone]
        )

        MessageThread(message).start()

    @staticmethod
    def send_welcome_email(request, user):
        current_site = f'{request.scheme}://{request.get_host()}'
        subject = 'Account Verified'
        message = render_to_string('accounts/welcomemessage.html', {
            'domain':current_site,
            'name':user.name, 
            'site_name': settings.SITE_NAME,
        })

        email_message = EmailMessage(subject=subject, body=message, to=[user.email])
        email_message.content_subtype = "html"
        
        MessageThread(email_message).start()