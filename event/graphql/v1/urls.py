from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from .schema import schema

urlpatterns = [
    path("", csrf_exempt(GraphQLView.as_view(
        graphiql=True
        # backend=GraphQLCustomCoreBackend(),
        # schema=schema
        ))),
]