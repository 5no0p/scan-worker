import uuid

# from django.utils.timezone import now
from django.conf import settings
from django.db import models

from core.mixins import BaseModel

class EventTicket(BaseModel):
    # id = models.UUIDField(
    #     default=uuid.uuid4,
    #     primary_key=True,
    #     editable=False,
    #     unique=True,
    #     verbose_name="Id"
    # )
    category = models.ForeignKey(
        'event.EventCategory',
        on_delete=models.CASCADE,
        verbose_name="Category",
        related_name="tickets"
    )
    owner = models.ForeignKey(
        'event.EventCustomer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Owner",
        related_name="tickets"
    )
    valid = models.BooleanField(
        default=False,
        verbose_name="Valid"
        )
    extra_fields = models.JSONField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.id}"

    def ticket_event(self):
        return self.category.event

    def ticket_checks(self):
        return self.checks.all()

    def ticket_checks_security_layers_levels(self):
        return list(self.ticket_checks().values_list('checked_by__event_security_layer__level', flat=True))

    def ticket_info(self):
        return {
        'ticket_id': self.id,
        'event_id': self.ticket_event().id,
        'event_name': self.ticket_event().name,
        'event_category_name': self.category.name,
        'event_category_id': self.category.id,
        'ticket_checks_ids': list(self.ticket_checks().values_list('id', flat=True)),
        'ticket_checked_by_ids': list(self.ticket_checks().values_list('checked_by__id', flat=True)),
        'ticket_checks_security_layers_levels': self.ticket_checks_security_layers_levels()
    }


class TicketCheck(BaseModel):
    ticket = models.ForeignKey(
        'event.EventTicket',
        on_delete=models.CASCADE,
        verbose_name="Ticket",
        related_name="checks"
    )
    checked_by = models.ForeignKey(
        'event.EventSecurityLayerMember',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Checked by",
        related_name="events_tickets_checks"
    )
    checked_in = models.DateTimeField(
        null=True,
        blank=True
        )
    checked_out = models.DateTimeField(
        null=True,
        blank=True
        )

    class Meta:
        ordering = ['-checked_in', '-checked_out']

    def __str__(self):
        return f"Ticket: {self.ticket.id} {'checked in' if self.checked_in else 'checked out'} - {self.checked_in if self.checked_in else self.checked_out}"
        # return f"{self.checked_in}"