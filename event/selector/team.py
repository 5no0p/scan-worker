import logging

from event.models import EventTeamMember

logger = logging.getLogger(__name__)

def get_event_team_member_by_id(event_team_member_id):
    try:
        event_team_member = EventTeamMember.objects.get(id=event_team_member_id)
        return event_team_member
    except EventTeamMember.DoesNotExist:
        EventTeamMember.DoesNotExist(f"Event Member with id: {event_team_member_id} does not exist.")