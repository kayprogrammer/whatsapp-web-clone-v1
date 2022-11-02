from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from apps.accounts.forms import MyAuthForm
from apps.common import views
from django.contrib.auth.views import LoginView

import debug_toolbar
# handler404 = views.handler404
# handler500 = views.handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('', include('apps.chat.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)