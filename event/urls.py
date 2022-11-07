from django.urls import path, re_path
from event.views import member_permissions

urlpatterns = [
    path('org/<uuid:org_id>', member_permissions),
]