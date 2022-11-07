import logging

from event.models import EventTicket

logger = logging.getLogger(__name__)

def get_event_ticket_by_id(event_ticket_id):
    try:
        event_ticket = EventTicket.objects.get(id=event_ticket_id)
        return event_ticket
    except EventTicket.DoesNotExist:
        EventTicket.DoesNotExist(f"Ticket with id: {event_ticket_id} does not exist.")