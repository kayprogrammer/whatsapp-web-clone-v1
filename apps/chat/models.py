from django.db import models
from django.contrib.auth import get_user_model

from apps.common.models import TimeStampedUUIDModel

User = get_user_model()

class Message(TimeStampedUUIDModel):
    sender = models.ForeignKey(User, related_name="sender_messages", on_delete=models.SET_NULL, null=True)
    receiver = models.ForeignKey(User, related_name="receiver_messages", on_delete=models.SET_NULL, null=True) 
    text = models.TextField(null=True, blank=True)
    vn = models.FileField(upload_to="whatsappclonev1/voicenotes/", null=True, blank=True)
    file = models.FileField(upload_to="whatsappclonev1/messagefiles/", null=True, blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message by {self.sender.name} to {self.receiver.name} : {self.text}"

    class Meta:
        ordering = ["-created_at"]

    