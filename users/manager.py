from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import UserManager
from django.db.models.query import QuerySet

class SoftDeleteUserQuerySet(QuerySet):
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

class SoftDeleteUserManager(UserManager):
    """
    Only exposes user objects that have NOT been soft-deleted.
    """
    def get_queryset(self):
        return SoftDeleteUserQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)

class DeletedUserQuerySet(QuerySet):

    """
    Restoe whatever objects you want to bring them back.
    """
    def restore(self, *args, **kwargs):
        qs = self.filter(*args, **kwargs)
        qs.update(is_deleted=False, deleted_at=None)

class DeletedUserManager(UserManager):
    """
    Show deleted user objects.
    """
    def get_queryset(self):
        return DeletedUserQuerySet(self.model, self._db).filter(deleted_at__isnull=False)


class GlobalUserManager(UserManager):

    """
    Expose all objects.
    """
    pass