
from django.urls import path

from strawberry.django.views import GraphQLView
from django_starter_app.schema import schema

urlpatterns = [
    path("graphql/", GraphQLView.as_view(schema=schema)),
]
