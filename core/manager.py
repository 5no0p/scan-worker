# from datetime import timezone

from django.utils import timezone
from django.db.models import Manager
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.query import QuerySet

class SoftDeleteQuerySet(QuerySet):
    """
    Prevents objects from being hard-deleted. Instead, sets the
    ``date_deleted``, effectively soft-deleting the object.

    For hard deleting objects, use super delete function instead.
    """

    def delete(self):
        for obj in self:
            obj.delete
        return self.update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

class SoftDeleteManager(Manager):
    """
    Only exposes objects that have NOT been soft-deleted.
    """
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)

class DeletedQuerySet(QuerySet):

    """
    Restoe whatever objects you want to bring them back.
    """
    def restore(self, *args, **kwargs):
        qs = self.filter(*args, **kwargs)
        qs.update(is_deleted=False, deleted_at=None)

class DeletedManager(BaseUserManager):
    """
    Show deleted user objects.
    """
    def get_queryset(self):
        return DeletedQuerySet(self.model, self._db).filter(deleted_at__isnull=False)


class GlobalManager(Manager):

    """
    Expose all objects.
    """
    pass

