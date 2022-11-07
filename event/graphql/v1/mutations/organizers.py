import graphene

from django.contrib.auth import get_user_model

from ..types import OrganizerType
from event.services import create_organizer

User = get_user_model()

class OrganizerCreateMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.UUID(required=True)
        short = graphene.String()

    organizer = graphene.Field(OrganizerType)

    @classmethod
    def mutate(cls, root, info, user_id, short):
        user = User.objects.get(id=user_id)
        organizer = create_organizer(organizer=user, short=short)
        return OrganizerCreateMutation(organizer=organizer)


class OrganizerMutation(graphene.ObjectType):
    create_organizer = OrganizerCreateMutation.Field()