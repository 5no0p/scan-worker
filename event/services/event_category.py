import logging

from django.utils import timezone

from core.exeptions import ModelCouldNotBeCreated
from event.lib import event_category_end_date
from event.models import EventCategory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_event_category(
    #event_id, name, price=0.00, start_at=None, end_at=None, description=None, color=None
    *args, **kwargs
    ) -> EventCategory:
    """
    Creates a new event category.
    :return: The newly created EventCategory
    :rtype: ~event.models.EventCategory
    :raises ModelCouldNotBeCreated: Could not create EventCategory object
    """
    
    try:
        event_category = EventCategory.objects.create(*args,**kwargs)
        logger.info(f"EventCategory('{event_category.name}') has been created for Event('{event_category.event.name}')")
        return event_category
    except ModelCouldNotBeCreated:
        logger.error("Could not create EventCategory")
        raise ModelCouldNotBeCreated("EventCategory could not be created")