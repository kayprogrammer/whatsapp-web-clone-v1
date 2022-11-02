import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedUUIDModel
from . managers import CustomUserManager

class Timezone(TimeStampedUUIDModel):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.name)

class PRIVACYCHOICES:
    last_seen = (
        ('EVERYONE', 'EVERYONE'),
        ('MY CONTACTS', 'MY CONTACTS'),
        ('NOBODY', 'NOBODY')
    )

    avatar_status = last_seen
    about_status = last_seen
    groups_status = last_seen

    message_timer = (
        ('24 HOURS', '24 HOURS'),
        ('7 DAYS', '7 DAYS'),
        ('90 DAYS', '90 DAYS'),
        ('OFF', 'OFF')
    )

THEME_CHOICES = (
    ('LIGHT', 'LIGHT'),
    ('DARK', 'DARK'),
    ('SYSTEM_DEFAULT', 'SYSTEM_DEFAULT')
)

class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(verbose_name=(_("Name")), max_length=50)
    email = models.EmailField(verbose_name=(_("Email address")), unique=True)
    phone = models.CharField(max_length=20, verbose_name=(_('Phone Number')), unique=True)
    tz = models.ForeignKey(Timezone, on_delete=models.SET_NULL, verbose_name=(_('Timezone')), null=True)
    avatar = models.ImageField(upload_to="whatsappclone/avatars/", null=True)
    theme = models.CharField(max_length=100, choices=THEME_CHOICES, null=True)
    wallpaper = models.ImageField(upload_to="whatsappclone/wallpapers/", null=True)
    status = models.CharField(default="Hey There! I'm using Whatsapp Web Clone V1!", max_length=300)

    #---Privacy Settings---#
    last_seen = models.CharField(default="EVERYONE", max_length=100, choices=PRIVACYCHOICES.last_seen)
    avatar_status = models.CharField(default="EVERYONE", max_length=100, choices=PRIVACYCHOICES.avatar_status)
    about_status = models.CharField(default="EVERYONE", max_length=100, choices=PRIVACYCHOICES.about_status)
    group_status = models.CharField(default="EVERYONE", max_length=100, choices=PRIVACYCHOICES.groups_status)
    message_timer = models.CharField(default="OFF", max_length=100, choices=PRIVACYCHOICES.message_timer)
    read_receipts = models.BooleanField(default=True)
    blocked_contacts = models.IntegerField(default="0")
    #----------------------#

    #---Notification Settings---#
    message_notifications = models.BooleanField(default=True)
    show_previews = models.BooleanField(default=True)
    show_reaction_notifications = models.BooleanField(default=True)
    sounds = models.BooleanField(default=True)
    security_notifications = models.BooleanField(default=True)
    #----------------------#

    terms_agreement = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["name", 'email']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    @property
    def avatarURL(self):
        try:
            url = self.avatar.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.name

class BlockedContact(TimeStampedUUIDModel):
    blocker = models.ForeignKey(User, related_name='blocker_blocked_contacts', on_delete=models.SET_NULL, null=True)
    blockee = models.ForeignKey(User, related_name='blockee_blocked_contacts', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        try:
            return f"{self.blocker.name} blocked {self.blockee.name}"
        except:
            return "Block issues"    

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['blocker', 'blockee'], 
            name='unique_blocker_blockee')
        ]