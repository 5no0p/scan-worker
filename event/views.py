import uuid
from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from event.selector import get_organizer_by_id, select_organizer_by_id_with_related

def member_permissions(request, org_id):
    organizer_by_id = get_organizer_by_id(org_id)
    events = organizer_by_id.events.all().first().categories.all().first()
    # select_time = connection.queries[-1]["time"]
    # organizer_by_id_with_related = select_organizer_by_id_with_related(org_id)#"32edf0a1-ff13-4f14-b45b-f04911b4319d"
    # select_releated_time = connection.queries[-1]["time"]
    return HttpResponse(
        f"<html><body><ul><li>{events}</li></ul></body></html>"
    )