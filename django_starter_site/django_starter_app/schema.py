from typing import Optional
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
import strawberry
from strawberry import auto

from strawberry.types import Info
from django_starter_app import models


@gql.django.type(models.UserProfile)
class UserProfile(relay.Node):
    country: str

    @strawberry.field
    def full_name(root: models.UserProfile, info: Info) -> str:
        return f"{root.user.first_name} {root.user.last_name}"


@gql.django.type(models.Blip)
class Blip(relay.Node):
    content: str
    author: UserProfile

    @classmethod
    def resolve_node(cls, node_id, info, required=False):
        return models.Blip.objects.get(id=node_id)

    @classmethod
    def resolve_nodes(cls, node_id, info, node_ids=False):
        pass


@gql.type
class Query:
    node: Optional[relay.Node] = relay.node()
    blip: Optional[Blip] = relay.node()


schema = strawberry.Schema(query=Query)
