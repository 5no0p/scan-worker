import graphene

from graphene_django.filter import DjangoFilterConnectionField

from ..types import EventType, EventTicketType, EventNode
from event.selector import (
    select_all_events, 
    select_even_by_id, 
    select_event_by_id_with_related,
    select_all_events_with_related,
    select_event_by_name_and_organizerId_with_related
    )
from event.services import get_event_by_name, get_event_tickets


class EventQuery(graphene.ObjectType):
    event = graphene.relay.Node.Field(EventNode)
    all_events = DjangoFilterConnectionField(EventNode)

    # all_events = graphene.List(EventType)
    event_by_id = graphene.Field(EventType, id=graphene.UUID(required=True))
    event_by_name = graphene.Field(EventType, name=graphene.String(required=True), organizer_id=graphene.UUID(required=True))
    event_tickets = graphene.List(EventTicketType, event_id=graphene.UUID(required=True))

    # def resolve_all_events(root, info):
    #     return select_all_events_with_related()

    def resolve_event_by_id(root, info, id):
        return select_event_by_id_with_related(id)

    def resolve_event_by_name(root, info, name, organizer_id):
        return select_event_by_name_and_organizerId_with_related(name, organizer_id)

    def resolve_event_tickets(root, info, event_id):
        return get_event_tickets(event_id)