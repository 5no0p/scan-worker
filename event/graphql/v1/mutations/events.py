import json

from django.core.serializers import serialize

import graphene

from event.selector import get_organizer_by_id, select_even_by_id
from event.services import create_event, create_event_category
from ..types import EventType, EventCategoryType


class EventCreateMutation(graphene.Mutation):
    event = graphene.Field(EventType)

    class Arguments:
        organizer_id = graphene.UUID(required=True)
        name = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, organizer_id, name):
        organizer = get_organizer_by_id(organizer_id)
        event = create_event(organizer=organizer, name=name)
  
        return EventCreateMutation(event=event)

    

class EventCategoryCreateMutation(graphene.Mutation):
    event_category = graphene.Field(EventCategoryType)
    
    class Arguments:
        event_id = graphene.UUID(required=True)
        name = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, event_id, name):
        event = select_even_by_id(event_id)
        event_category = create_event_category(event=event, name=name)
        return EventCategoryCreateMutation(event_category=event_category)



class EventMutation(graphene.ObjectType):
    create_event = EventCreateMutation.Field()
    create_event_category = EventCategoryCreateMutation.Field()