import logging

from celery import shared_task


logger = logging.getLogger(__name__)

@shared_task(bind=True)
def ticket_check_in(self, ticket_id, checked_by, check_datetime, check_type):
    from event.services import new_ticket_check

    return new_ticket_check(ticket_id, checked_by, check_datetime, check_type)