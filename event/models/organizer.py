import uuid

from django.conf import settings
from django.utils.translation import gettext_lazy as _ #ugettext_lazy for django 3.2
from django.db import models

from core.mixins import BaseModel

class Organizer(BaseModel):
    organizer = models.OneToOneField(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name='organizing',
            verbose_name=_('Organizer')
            )
    short = models.CharField(
            max_length=100, 
            null=True, 
            blank=True
            )
    slug = models.SlugField(null=True, blank=True)