from event.models import EventSecurityLayer
from event.selector import get_event_security_layer_by_id

def previous_event_security_layer(event_security_layer):
    if event_security_layer.level > 1:
        #event_security_layer = get_event_security_layer_by_id(event_scurity_layer_id)
        previous_event_security_layer=EventSecurityLayer.objects.filter(event=event_security_layer.event,level__lt=event_security_layer.level).order_by('level').last()
        return previous_event_security_layer
    return {
        "error": {"level_value":"EventSecurityLayer level must be more than 1"}
    } 

def get_previous_event_security_layer(event_scurity_layer_id):
    event_security_layer = get_event_security_layer_by_id(event_scurity_layer_id)
    return previous_event_security_layer(event_security_layer)


def get_first_event_security_layer(event):
    return EventSecurityLayer.objects.filter(event=event).order_by('level').first()

def check_first_event_security_layer_level(event_security_layer):
    return event_security_layer.level == get_first_event_security_layer(event_security_layer.event).level