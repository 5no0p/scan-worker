import uuid

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import TrakingModel

from users.manager import SoftDeleteUserManager, DeletedUserManager, GlobalUserManager


class SoftDeleteUserModel(models.Model):
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='deleted_%(app_label)s_%(class)s_by_me', 
        related_query_name="%(app_label)s_%(class)ss", null=True, 
        blank=True, verbose_name=_('Deleted by')
        )
    deleted_at = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name=_('Deleted at')
        )

    objects = SoftDeleteUserManager()
    deleted_objects = DeletedUserManager()
    global_objects = GlobalUserManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()
        self.after_delete()

    def restore(self):
        self.deleted_at = None
        self.save()
        self.after_restore()

class User(SoftDeleteUserModel, TrakingModel, AbstractUser):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        unique=True,
    )
