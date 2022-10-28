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

class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(verbose_name=(_("Name")), max_length=50)
    email = models.EmailField(verbose_name=(_("Email address")), unique=True)
    phone = models.CharField(max_length=20, verbose_name=(_('Phone Number')), unique=True)
    tz = models.ForeignKey(Timezone, on_delete=models.SET_NULL, verbose_name=(_('Timezone')), null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["name", 'email']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.name
