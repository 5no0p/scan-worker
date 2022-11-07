import logging

from event.exeptions import ModelIdNotProvided
from event.models import Event


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def select_even_by_id(event_id) -> Event: 
    try:
        if not event_id:
            raise ModelIdNotProvided("Please provide an event id")
        selected_event = Event.objects.get(id=event_id)
        logger.info("Select Event with id(%s)", selected_event.id)
        return selected_event
    except Event.DoesNotExist:
        logger.error("Cannot find Event for event_id: %s", event_id)
        raise Event.DoesNotExist("Event with id: %s dose not exist" % event_id)

def select_all_events():
    try:
        events = Event.objects.select_related('organizer').all()
        return events
    except Event.DoesNotExist:
        raise Event.DoesNotExist("Events not available")

def select_all_events_with_related():
    return Event.objects.select_related('organizer').all()

def select_event_by_id_with_related(event_id):
    try:
        return Event.objects.select_related('organizer').get(id=event_id)
    except Event.DoesNotExist:
        raise Event.DoesNotExist(f"Event with id ({event_id}) not available" )

def select_event_by_name_and_organizerId_with_related(event_name, organizer_id):
    try:
        return Event.objects.select_related('organizer').filter(name=event_name, organizer=organizer_id)
    except Event.DoesNotExist:
        raise Event.DoesNotExist(f"Events with name ({event_name}) for organizer with id ({organizer_id}) not available" )