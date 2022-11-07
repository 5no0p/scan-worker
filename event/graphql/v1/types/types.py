import graphene

from graphene_django import DjangoObjectType

from event.models import (
    Organizer, 
    Event, 
    EventCategory, 
    EventTicket, 
    EventCustomer, 
    TicketCheck,
    EventSecurityLayer,
    EventSecurityLayerMember,
    SecurityLayer,
    EventTeam,
    EventTeamMember,
    Team,
    TeamMember
    )

        
class OrganizerType(DjangoObjectType):
    class Meta:
        model = Organizer
        #fields = ['id', 'organizer', 'short']

class OrganizerNode(DjangoObjectType):
    class Meta:
        model = Organizer
        filter_fields = [
            'id',
            'organizer',
            'short'
        ]
        interfaces = (graphene.relay.Node, )

class EventType(DjangoObjectType):
    class Meta:
        model = Event
        #fields = ['id', 'organizer', 'name', 'start_at', 'end_at', 'description', 'timezone']

class EventNode(DjangoObjectType):
    class Meta:
        model = Event
        filter_fields = {
            'organizer':['exact'],
            'name':['exact', 'icontains', 'istartswith'], 
            'start_at':['exact', 'icontains', 'istartswith'], 
            'end_at':['exact', 'icontains', 'istartswith'], 
            #'timezone'
            }
        interfaces = (graphene.relay.Node, )

class EventCategoryType(DjangoObjectType):
    class Meta:
        model = EventCategory
        #fields = ['id', 'event', 'name', 'start_at', 'end_at', 'description', 'price']

class EventTicketType(DjangoObjectType):
    class Meta:
        model = EventTicket
        #fields = ['id', 'category', 'owner', 'valid', 'extra_#fields', 'checks']

class EventCustomerType(DjangoObjectType):
    class Meta:
        model = EventCustomer
        #fields = ['id', 'event', 'name', 'email', 'phone']

class TicketCheckType(DjangoObjectType):
    class Meta:
        model = TicketCheck
        #fields = ['id', 'ticket', 'checked_by', 'checked_in', 'checked_out']

class EventSecurityLayerType(DjangoObjectType):
    class Meta:
        model = EventSecurityLayer
        #fields = ['id', 'event', 'security_layer']

class EventSecurityLayerMemberType(DjangoObjectType):
    class Meta:
        model = EventSecurityLayerMember
        #fields = ['id', 'event_security_layer', 'member']

class SecurityLayerType(DjangoObjectType):
    class Meta:
        model = SecurityLayer
        #fields = ['id', 'name', 'organizer']

class EventTeamType(DjangoObjectType):
    class Meta:
        model = EventTeam
        #fields = ['id', 'event', 'name', 'color']

class EventTeamMemberType(DjangoObjectType):
    class Meta:
        model = EventTeamMember
        #fields = ['id', 'event_team', 'member']

class TeamType(DjangoObjectType):
    class Meta:
        model = Team
        #fields = ['id', 'name', 'organizer', 'slag']

class TeamMemberType(DjangoObjectType):
    class Meta:
        model = TeamMember
        #fields = ['id', 'team', 'member']