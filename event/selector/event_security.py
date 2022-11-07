import logging

from event.exeptions import ModelIdNotProvided
from event.models import EventSecurityLayer, EventSecurityLayerMember

logger = logging.getLogger(__name__)

def get_event_security_layer_by_id(event_security_layer_id):
    try:
        if not event_security_layer_id:
            raise ModelIdNotProvided("Please provide EventSecurityLayer id")
        selected_event = EventSecurityLayer.objects.get(id=event_security_layer_id)
        logger.info("Select EventSecurityLayer with id(%s)", selected_event.id)
        return selected_event
    except EventSecurityLayer.DoesNotExist:
        logger.error("Cannot find EventSecurityLayer for event_security_layer_id: %s", event_security_layer_id)
        raise EventSecurityLayer.DoesNotExist("EventSecurityLayer with id: %s dose not exist" % event_security_layer_id)


def get_event_security_layer_member_by_id(security_layer_member_id):
    try:
        if not security_layer_member_id:
            raise ModelIdNotProvided("Please provide EventSecurityLayerMember id")
        selected_event = EventSecurityLayerMember.objects.get(id=security_layer_member_id)
        logger.info("Select EventSecurityLayerMember with id(%s)", selected_event.id)
        return selected_event
    except EventSecurityLayerMember.DoesNotExist:
        logger.error("Cannot find EventSecurityLayerMember for security_layer_member_id: %s", security_layer_member_id)
        raise EventSecurityLayerMember.DoesNotExist("EventSecurityLayerMember with id: %s dose not exist" % security_layer_member_id)