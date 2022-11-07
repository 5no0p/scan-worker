from event.models import EventPermission

def get_event_permission_by_id(permission_id):
     
     return EventPermission.objects.get(id=permission_id)