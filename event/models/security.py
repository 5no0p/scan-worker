import uuid

from django.utils.translation import gettext_lazy as _
from django.db import models

from core.mixins import BaseModel


class EventSecurityLayer(BaseModel):
    event = models.ForeignKey(
        'event.Event',
        on_delete=models.CASCADE
    )
    security_layer = models.ForeignKey(
        'event.SecurityLayer',
        on_delete=models.CASCADE,
    )
    level = models.PositiveIntegerField()

class EventSecurityLayerMember(BaseModel):
    event_security_layer = models.ForeignKey(
        'event.EventSecurityLayer',
        on_delete=models.CASCADE,
        related_name='members',
    )
    member = models.ForeignKey(
        'event.EventTeamMember',
        on_delete=models.CASCADE,
        related_name='event_security_layers',
    )

    def previous_security_layer_level(self):
        from event.services import previous_event_security_layer
        return previous_event_security_layer(self.event_security_layer)

class SecurityLayer(BaseModel):
    # id = models.UUIDField(
    #     default=uuid.uuid4, 
    #     primary_key=True, 
    #     editable=False,
    #     unique=True,
    #     verbose_name="Id"
    #     )
    name = models.CharField(
        max_length=100,
        verbose_name=_('Name'),
    )
    organizer = models.ForeignKey(
        'event.Organizer',
        on_delete=models.CASCADE
    )

class SecurityLayerMember(BaseModel):
    security_layer = models.ForeignKey(
        SecurityLayer,
        on_delete=models.CASCADE,
        related_name='security_layer_members'
        )
    member = models.ForeignKey(
        'event.TeamMember',
        on_delete=models.CASCADE,
        related_name='security_layers' 
    )