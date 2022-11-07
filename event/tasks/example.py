import logging

from celery import shared_task, chain

logger = logging.getLogger(__name__)

@shared_task
def adding(x, y):
    return x + y

@shared_task
def create_event_with_default_settings(organizer_id, event_name):
    # from event.models import Organizer
    # from event.services.event import create_event
    # from event.services.event_category import create_event_category
    # from event.services.tickets import generate_tickets_for_event_category

    # event = create_event(organizer=Organizer.objects.get(id=f"{organizer_id}"), name=event_name)
    # event_category = create_event_category(event=event, name='default')
    # event_category_tickets = generate_tickets_for_event_category(event_category.id)
    # logger.info(f"Event has been created with default settings:\n"+
    # f"Event: {event}\n"+
    # f"Event category: {event_category}\n"+
    # f"Event category tickets: {event_category_tickets}")

    from event.tasks import (
        create_new_event,
        create_new_event_category,
        geneate_event_category_tickets
    )

    res = chain(
        create_new_event.s(organizer_id, event_name), 
        create_new_event_category.s('catrgory'), 
        geneate_event_category_tickets.s(15)
        )()
    return res