from django.contrib import admin
from django.utils.safestring import mark_safe

admin.site.site_header = mark_safe('<strong style="font-weight:bold;">WWC V1 ADMIN</strong>')