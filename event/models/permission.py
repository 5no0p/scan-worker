import uuid

from django.db import models

from core.mixins import BaseModel
class EventPermission(BaseModel):
    # id = models.UUIDField(
    #     default = uuid.uuid4,
    #     primary_key = True,
    #     editable = False,
    #     unique=True,
    #     verbose_name="Id"
    # )
    name = models.CharField(
        max_length = 200,
    )
    code = models.CharField(
        max_length = 200,
    )
    color = models.CharField(
        max_length = 10,
    )

    def __str__(self) -> str:
        return f"{self.name}"