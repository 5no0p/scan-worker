import logging

from core.exeptions import ModelCouldNotBeCreated
from event.models import Event

logger = logging.getLogger(__name__)

def create_event(*args, **kwargs):
    """
    Create a new event.

    :return: The newly created Event
    :rtype: ~event.models.Event
    :raises ModelCouldNotBeCreated: Could not create Event object
    """
    try:
        event = Event.objects.create(*args, **kwargs)
        return event
    except ModelCouldNotBeCreated:
        logger.error("Could not create Event object")
        raise ModelCouldNotBeCreated("Could not create Event object")

def create_new_event():
    pass


def get_event_by_name(name):
    try:
        return Event.objects.get(name=name)
    except Event.DoesNotExist:
        return None
