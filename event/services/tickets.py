import logging

from django.db.models import Max

from core.exeptions import ModelIdNotProvided, ModelCouldNotBeCreated
from event.exeptions import (
    GeneratedTicketsNumberLessThanOne,
    TicketsNotGenerated,
    TicketsNotBeenAddedToCategory
    )
from event.selector import (
    get_event_category_by_id, 
    get_event_ticket_by_id,
    get_event_security_layer_member_by_id
)
from event.services.security import (
    previous_event_security_layer, 
    check_first_event_security_layer_level
    )
from users.selector import get_user_by_id
from event.models import (
    EventTicket,
    EventSecurityLayerMember,
    TicketCheck
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_tickets(tickets_number=1):
    """
    Generates tickets for the given number of tickets.

    :param int tickets_number: Number of tickets to generate.
    :return: List of tickets
    :rtype: list
    :raises TicketsNotGenerated: Could not generate tickets
    """
    if tickets_number < 1:
        raise GeneratedTicketsNumberLessThanOne("Please provide a number of tickets more than 0")
    
    try:
        generate_tickets = [EventTicket() for number in range(tickets_number)]
        logger.info(f"Generate {tickets_number} ticket{'s'[:tickets_number^1]}")
        return generate_tickets
    except TicketsNotGenerated:
        raise TicketsNotGenerated("Could not generate tickets")


def generate_tickets_for_event_category(category_id, tickets_number=1):
    """
    Generates tickets for a given event category.

    :param int category_id: Event category id
    :param int tickets_number: Number of tickets to generate.
    :raises TicketsNotBeenAddedToCategory: Could add tickets to a category
    """

    if not category_id:
        raise ModelIdNotProvided("Please provide a category identifier")

    if tickets_number < 1:
        raise GeneratedTicketsNumberLessThanOne("Please provide a number of tickets more than 0")

    event_category = get_event_category_by_id(category_id)
    generated_tickets = generate_tickets(tickets_number)
    try:
        event_category.tickets.add(*generated_tickets, bulk=False)
        logger.info(f"Add ({len(generated_tickets)}) ticket{'s'[:len(generated_tickets)^1]} to Event Category with id({event_category.id})")
        return [ticket.id for ticket in generated_tickets]
        
    except TicketsNotBeenAddedToCategory:
        raise TicketsNotBeenAddedToCategory("Tickets not added to category with id(%s)" % category_id)

def get_ticket_last_check(ticket_id):
    return TicketCheck.objects.filter(ticket__id=ticket_id).aggregate(last_checked_out=Max('checked_out'),last_checked_in=Max('checked_in'))

def get_security_layer_ticket_last_check(ticket_id, security_layer_id):
    return TicketCheck.objects.filter(ticket__id=ticket_id, checked_by__event_security_layer__id=security_layer_id).aggregate(last_checked_out=Max('checked_out'),last_checked_in=Max('checked_in'))

def create_ticket_check(*args, **kwargs):

    ticket_check = TicketCheck.objects.create(*args, **kwargs)
    return ticket_check

def new_ticket_check(ticket_id, checker_id, checker_datetime, check_type: str='checked_in'):
    """
    Creates a new ticket check.
    
    :param uuid ticket_id: EventTicket id
    :param uuid checker_id: EventTeamMember id
    :param datetime.datetime check_in_datetime: EventTicket datetime
    :raises TicketCouldNotBeCreated: Could not create TicketCheck
    """

    # States for check_type
    check_state = {
        'checked_in': {
            'other': 'checked_out',
            'name': 'checked_in'
        },
        'checked_out': {
            'other': 'checked_in',
            'name': 'checked_out'
        }
    }

    try:
        ticket = get_event_ticket_by_id(ticket_id)
        ticket_info = ticket.ticket_info()
        
        try:    
            checked_by = get_event_security_layer_member_by_id(checker_id)
            ticket_last_check = get_security_layer_ticket_last_check(ticket_id, checked_by.event_security_layer.id)
            
            def _ticket_check_create_process():

                # Check if if this scurity layer the first one.
                # If not check if the previous one has checked this ticket before.
                if check_first_event_security_layer_level(checked_by.event_security_layer) or previous_event_security_layer(checked_by.event_security_layer).level in ticket_info['ticket_checks_security_layers_levels']:

                    # Create the check kwargs.
                    ticket_check_kwargs = {
                        'ticket':ticket, 
                        'checked_by':checked_by,
                        check_type:checker_datetime
                    }

                    try:
                        ticket_check = create_ticket_check(**ticket_check_kwargs)
                        return ticket_check

                    except ModelCouldNotBeCreated:
                        ModelCouldNotBeCreated(f"TicketCheck model could not be created with thies params.\n"+
                        f"- ticket_id: {ticket_id}\n"+f"- checked_by: {checker_id}\n"+f"- {check_type}: {checker_datetime}"
                        )
                else:
                    raise Exception('This ticket must be checked in the previous security level')

            if check_type == 'checked_in':
                if ticket_last_check['last_checked_in'] is None: 
                    return _ticket_check_create_process()
                else:
                    raise Exception('This ticket already checked in')
            elif check_type == 'checked_out':
                if ticket_last_check['last_checked_in'] is not None:
                    if ticket_last_check['last_checked_out'] is None: 
                        #return _ticket_check_create_process()
                        ticket_check = TicketCheck.objects.filter(ticket__id=ticket_id, checked_by__id=checker_id).update(checked_out=checker_datetime)
                        return ticket_check
                    else:
                        raise Exception('This ticket already checked out')
                else:
                    raise Exception('This ticket should be checked in before check it out')
            else:
                raise Exception('Check type should be checked_in either checked_out')                
        except EventSecurityLayerMember.DoesNotExist:
            raise EventSecurityLayerMember.DoesNotExist(f'SecurityLayerMember with id: {checker_id} dose not exist')
    except EventTicket.DoesNotExist:
        raise EventTicket.DoesNotExist(f'EventTicket with id: {ticket_id} dose not exist')

def get_ticket_info(ticket_id):
    ticket = get_event_ticket_by_id(ticket_id)
    ticket_event = ticket.ticket_event()
    ticket_checks = ticket.ticket_checks()
 
    return {
        'ticket_id': ticket.id,
        'event_id': ticket_event.id,
        'event_name': ticket_event.name,
        'event_category_name': ticket.category.name,
        'event_category_id': ticket.category.id,
        'ticket_checks_ids': list(ticket_checks.values_list('id', flat=True)),
        'ticket_checked_by_ids': list(ticket_checks.values_list('checked_by__id', flat=True)),
        'ticket_checks_security_layers_levels': list(ticket_checks.values_list('checked_by__event_security_layer__level', flat=True))
    }

def get_event_tickets(event):
    return EventTicket.objects.filter(category__event=event)