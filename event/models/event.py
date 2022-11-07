import uuid
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone

from timezone_field import TimeZoneField

from core.mixins import BaseModel

from event.lib import event_end_date, event_category_end_date

class Event(BaseModel):
    name = models.CharField(
        max_length = 200,
        verbose_name = _('Name'),
    )
    organizer = models.ForeignKey(
        'event.Organizer',
        on_delete=models.CASCADE,
        verbose_name=_('Organizer'),
        related_name='events',
    )
    start_at = models.DateTimeField(
        default=timezone.now,
        verbose_name = _('Start Date'),
        )
    end_at = models.DateTimeField(
        default=event_end_date,
        verbose_name = _('End Date'),
        )
    description = models.TextField(
        null=True, 
        blank=True,
        verbose_name = _('Description')
    )
    timezone = TimeZoneField(
        default='Africa/Cairo',
        verbose_name=_('TimeZone')
        )
    #location --> Location Model 

    def __str__(self) -> str:
        return f'{self.name}'

    def clean(self):
        if self.start_at > self.end_at:
            raise ValidationError('Event must start before end')


class EventCategory(BaseModel):
    # id = models.UUIDField(
    #     default = uuid.uuid4,
    #     primary_key = True,
    #     editable = False,
    #     unique=True,
    #     verbose_name="Id"
    # )
    event = models.ForeignKey(
        'event.Event',
        on_delete=models.CASCADE,
        verbose_name = _('Event'),
        related_name="categories"
    )
    name = models.CharField(
        max_length = 200,
        verbose_name=_('Name')
    )
    start_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Start Date')
        )
    end_at = models.DateTimeField(
        default=event_category_end_date,
        verbose_name=_('End Date')
        )
    description = models.TextField(
        null=True, 
        blank=True,
        verbose_name=_('Description')
        )
    price = models.DecimalField(
        default=Decimal("0.00"),
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Price'), 
    )

    color = models.CharField(
        _('Color'), 
        max_length=10,
        null=True,
        blank=True,
        )

    def clean(self):
    
        if self.start_at and self.end_at is not None and self.start_at > self.end_at:
            raise ValidationError({
                'start_at':'Event must start before end'})
        
        if self.end_at is not None and self.end_at > self.event.end_at:
            raise ValidationError({
                'end_at':'Event category must not end after event end'})
        if self.start_at is not None and self.start_at < self.event.start_at:
            raise ValidationError({
                'start_at':'Event category must not start before event start'})
        