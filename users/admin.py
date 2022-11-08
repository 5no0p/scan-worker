from django.contrib import admin
from django.apps import apps

from users.models import User

admin.site.register(User)
