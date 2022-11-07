import graphene

from ..types import OrganizerType
from event.selector import select_organizer_by_id_with_related, select_all_organizers



class OrganizerQuery(graphene.ObjectType):
    all_organizers = graphene.List(OrganizerType)
    organizer_by_id = graphene.Field(OrganizerType, id=graphene.UUID(required=True))

    def resolve_all_organizers(root, info):
        return select_all_organizers()

    def resolve_organizer_by_id(root, info, id):
        return select_organizer_by_id_with_related(id)