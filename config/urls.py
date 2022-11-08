from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('event.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
