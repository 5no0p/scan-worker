import graphene

from django.contrib.auth import get_user_model

from graphene_django import DjangoObjectType
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery

from .queries import OrganizerQuery, EventQuery
from .mutations import OrganizerMutation, EventMutation


User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class Query(UserQuery, MeQuery, OrganizerQuery, EventQuery, graphene.ObjectType):
    pass


class AuthMutation(graphene.ObjectType):
   register = mutations.Register.Field()
   verify_account = mutations.VerifyAccount.Field()
   token_auth = mutations.ObtainJSONWebToken.Field()
   update_account = mutations.UpdateAccount.Field()

class Mutation(
    AuthMutation, 
    OrganizerMutation, 
    EventMutation,
    graphene.ObjectType
    ):
   pass



schema = graphene.Schema(query=Query, mutation=Mutation)

