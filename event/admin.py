from django.contrib import admin

from core.admin import BaseAdminModel
from event.models import (
    Organizer,
    Event, 
    EventCategory,
    EventTicket,
    SecurityLayer,
    EventSecurityLayer,
    EventSecurityLayerMember,
    EventTeamMember,
    EventTeam,
    Team,
    TeamMember,
    TicketCheck,
    EventPermission,
    EventTeamPermission
)
from event.models.team import TeamMember

class EventTicketInline(admin.TabularInline):
    model = EventTicket
    fields = ["valid"]
    show_change_link = True

class EventCategoryInline(admin.TabularInline):
    model = EventCategory
    show_change_link = True
    
class OrganizerAdmin(BaseAdminModel):
    pass

class EventAdmin(BaseAdminModel):
    inlines = [
        EventCategoryInline,
    ]

class EventCategoryAdmin(BaseAdminModel):
    inlines = [
        EventTicketInline,
    ]

class EventTicketAdmin(BaseAdminModel):
    pass
class EventSecurityLayerAdmin(BaseAdminModel):
    pass

class EventTeamMemberAdmin(BaseAdminModel):
    pass


admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(EventTicket, EventTicketAdmin)
admin.site.register(EventSecurityLayer, EventSecurityLayerAdmin)
admin.site.register(EventTeam)
admin.site.register(EventTeamMember)
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(TicketCheck)
admin.site.register(EventPermission)
admin.site.register(EventTeamPermission)
admin.site.register(EventSecurityLayerMember)
admin.site.register(SecurityLayer)


