import logging

from event.exeptions import ModelIdNotProvided
from event.models import EventCategory


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_event_category_by_id(event_category_id) -> EventCategory: 
    """
    Get event category by id

    :param event_category_id: event category id
    :return: EventCategory
    :raises EventCategory.DoesNotExist: event category not found
    """
    try:
        if not event_category_id:
            raise ModelIdNotProvided("Please provide a category identifier")
        event_category = EventCategory.objects.get(id=event_category_id)
        logger.info("Select Event Category with id(%s)", event_category.id)
        return event_category
    except EventCategory.DoesNotExist:
        logger.error("Cannot find Event Category for event_category_id: %s", event_category_id)
        raise EventCategory.DoesNotExist("Event Category with id: %s dose not exist" % event_category_id)