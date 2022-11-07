import logging

from celery import shared_task

from core.exeptions import ModelCouldNotBeCreated

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def create_new_event(self, organizer_id, event_name):
    from event.models import Organizer
    from event.services.event import create_event

    try:
        new_event = create_event(organizer=Organizer.objects.get(id=f"{organizer_id}"), name=event_name)
        return new_event.id
    except Exception as exc:
        raise self.retry(exc=exc)

@shared_task(bind=True)
def create_new_event_category(self, event_id, category_name):
    from event.models import Event
    from event.selector.event import select_even_by_id
    from event.services.event_category import create_event_category
    try:
        event = select_even_by_id(event_id)
        new_event_category = create_event_category(event=event, name=category_name)
        return new_event_category.id
    except Exception as exc:
        raise self.retry(exc=exc)

@shared_task(bind=True)
def geneate_event_category_tickets(self, event_category_id, number_of_tickets):
    from event.services.tickets import generate_tickets_for_event_category
    try:
        new_event_category_tickets = generate_tickets_for_event_category(event_category_id, number_of_tickets)
        return new_event_category_tickets
    except Exception as exc:
        raise self.retry(exc=exc)