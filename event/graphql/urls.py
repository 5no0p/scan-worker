from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
        path("v1/", include('event.graphql.v1.urls')),

]