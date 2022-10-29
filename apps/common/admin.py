from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.accounts.forms import MyAuthForm

admin.site.site_header = mark_safe('<strong style="font-weight:bold;">WWC V1 ADMIN</strong>')
admin.site.login_form = MyAuthForm