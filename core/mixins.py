import uuid
from django.db import models
from .models import SoftDeleteModel, TrakingModel

class BaseModel(SoftDeleteModel, TrakingModel):
    id = models.UUIDField(
        default = uuid.uuid4,
        primary_key = True,
        editable = False,
        unique=True,
        verbose_name="Id"
    )
    class Meta:
        abstract = True
        ordering = ["created_at"]