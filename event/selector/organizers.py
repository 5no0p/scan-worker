from django.db.models import Prefetch

from event.models import (
    Organizer,
    Event, 
    EventTicket, 
    EventCategory
    )

def select_all_organizers():
    try:
        return Organizer.objects.all()
    except Exception as e:
        raise Exception(e)

def get_organizer_by_id(organizer_id):
    try:
        organizer = Organizer.objects.get(id=organizer_id)
        return organizer
    except Organizer.DoesNotExist:
        raise Organizer.DoesNotExist(f'Could not find Organizer with id: {organizer_id}')

# def get_organizer_with_events(organizer_id, events, categories, tickets, checks):
#     try:
#         organizer = Organizer.objects.prefetch_related('events').get(id=organizer_id)
#         return organizer
#     except Organizer.DoesNotExist:
#         raise Organizer.DoesNotExist(f'Could not find Organizer with id: {organizer_id}')

def select_organizer_by_id_with_related(organizer_id):
    try:
        prefetch_tickets = Prefetch('tickets', queryset=EventTicket.objects.prefetch_related('checks'))
        prefetch_categories = Prefetch('categories', queryset=EventCategory.objects.prefetch_related(prefetch_tickets))
        prefetch_events = Prefetch('events', queryset=Event.objects.prefetch_related(prefetch_categories))
        # prefetch_customers = Prefetch('customers', queryset=Event.objects.prefetch_related(prefetch_categories))
        return Organizer.objects.select_related('organizer').prefetch_related(
            prefetch_events, 
            # prefetch_customers
            ).get(id=organizer_id)
    except Organizer.DoesNotExist:
        raise Organizer.DoesNotExist(f'Could not find Organizer with related with id: {organizer_id}')
