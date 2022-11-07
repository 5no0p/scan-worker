import datetime

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from django.db import models

from .manager import SoftDeleteManager, DeletedManager, GlobalManager

class TrakingModel(models.Model):
    """
    Track model for create, update and delete actions.
    """
    created_at = models.DateField(default=datetime.date.today, null=True, blank=True,verbose_name=_('Created at'))
    updated_at = models.DateField(auto_now=True, null=True, blank=True, verbose_name=_('Updated at'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='creted_%(app_label)s_%(class)s_by_me', related_query_name="%(app_label)s_%(class)ss", null=True, blank=True, verbose_name=_('Created by'))
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='updated_%(app_label)s_%(class)s_by_me', related_query_name="%(app_label)s_%(class)ss", null=True, blank=True, verbose_name=_('Updated by'))
    
    
    # objects = SoftDeleteManager()
    # all_objects = models.Manager()
    
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class SoftDeleteModel(models.Model):
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

    objects = SoftDeleteManager()
    deleted_objects = DeletedManager()
    global_objects = GlobalManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()
        #self.after_delete()

    def restore(self):
        self.deleted_at = None
        self.save()
        #self.after_restore()