import uuid

from django.db import models

from core.mixins import BaseModel

class EventCustomer(BaseModel):
    event = models.ForeignKey(
        'event.Event',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Event",
        related_name="customers"
    )
    organizer = models.ForeignKey(
        'event.Organizer',
        on_delete=models.CASCADE,
        verbose_name="Organizer",
        related_name="customers"
    )
    name = models.CharField(
        max_length=255,
    )
    email = models.EmailField(
        max_length=255,
        null=True,
        blank=True
    )
    phone = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
