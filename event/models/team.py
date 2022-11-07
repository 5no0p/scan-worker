import uuid

from django.conf import settings
from django.utils.translation import gettext_lazy as _ 
from django.db import models

from core.mixins import BaseModel

class EventTeam(BaseModel):
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
        verbose_name="Event",
        related_name="teams",
    )
    name = models.CharField(
        max_length = 200,
    )
    color = models.CharField(
        max_length = 10,
    )

class EventTeamMember(BaseModel):
    event_team = models.ForeignKey(
        'event.EventTeam',
        on_delete=models.CASCADE,
        verbose_name=_('Event Team'),
        related_name='members',
    )
    member = models.ForeignKey(
        'event.TeamMember',
        on_delete=models.CASCADE,
        verbose_name=_('Member'),
        related_name='events_teams',
    )

    def __str__(self) -> str:
        return f"{self.member.member.username}"

    def member_permissions(self):
        permissions = []
        for permission in self.event_team.permissions.all():
            permissions.append(permission.permission)
        return permissions

    def check_member_permission_by_code(self, code: str) -> bool:
        permissions = self.member_permissions()
        return any(permission.code == code for permission in permissions)

    def get_event(self):
        return self.event_team.event

class EventTeamPermission(BaseModel):
    event_team = models.ForeignKey(
        'event.EventTeam',
        on_delete=models.CASCADE,
        verbose_name=_('Event Team'),
        related_name='permissions',
    )
    permission = models.ForeignKey(
        'event.EventPermission',
        on_delete=models.CASCADE,
        verbose_name=_('Permission'),
        related_name='events_teams',
    )

class Team(models.Model):
    # id = models.UUIDField(
    #         primary_key = True,
    #         default = uuid.uuid4,
    #         editable = False,
    #         unique=True,
    #         verbose_name="Id"
    #     )
    name = models.CharField(max_length=100)
    organizer = models.ForeignKey(
        'event.Organizer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teams',
        verbose_name=_('Team')
    )
    slag = models.SlugField( #auto add uuid orgnizer to slug ex. megdaed_team_115698
            max_length=150,  
            unique=True
    )

class TeamMember(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        verbose_name=_('Team'),
        related_name='members',
    )
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Member'),
        related_name='teams',
    )