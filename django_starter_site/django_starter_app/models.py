import uuid
from ast import Num, Str
from datetime import datetime
from email.policy import default
from enum import Enum

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import F
from django.db.models.fields import DateField, DateTimeField, related
from django.forms import NullBooleanSelect
from django.utils import timezone

# Create your models here.


class BaseDjangoGraphQLStarterModel(models.Model):

    def __repr__(self):
        return str(self.to_dict())

    # https://docs.djangoproject.com/en/4.0/topics/db/queries/#copying-model-instances
    def clone_no_save(self):
        self.pk = None
        self.id = None
        self._state.adding = True
        return self

    def to_dict(self):
        opts = self._meta
        data = {}
        for f in opts.concrete_fields + opts.many_to_many:
            if isinstance(f, models.ManyToManyField):
                if self.pk is None:
                    data[f.name] = []
                else:
                    data[f.name] = list(f.value_from_object(
                        self).values_list('pk', flat=True))
            elif isinstance(f, DateTimeField) and f.value_from_object(self) is not None:
                data[f.name] = f.value_from_object(
                    self).strftime('%Y-%m-%d %H:%M:%S%z')
            elif isinstance(f, DateField) and f.value_from_object(self) is not None:
                data[f.name] = f.value_from_object(self).strftime('%Y-%m-%d')
            else:
                val = f.value_from_object(self)
                data[f.name] = val
        return data

    # Auto time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(BaseDjangoGraphQLStarterModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_profile')
    country_code = models.CharField(max_length=2, default="", blank=True)

    class Meta:
        index_together = [
            ("user_id", "id"),
        ]


class Blip(BaseDjangoGraphQLStarterModel):
    """ 
    A short statement to the world, where the user is hopefully not a "pigeon".
    """
    author = models.ForeignKey(
        UserProfile, null=False, related_name='all_blips', on_delete=models.CASCADE)

    content = models.TextField()

    class Meta:
        index_together = [
            ("created_at", "id"),
        ]


class Comment(BaseDjangoGraphQLStarterModel):
    """ 
    A comment replying to an existing Blip
    """
    blip = models.ForeignKey(
        Blip, null=False, related_name='comments',  on_delete=models.CASCADE)
    author = models.ForeignKey(
        UserProfile, null=False, related_name='all_comments',  on_delete=models.CASCADE)

    comment = models.TextField()

    class Meta:
        index_together = [
            ("blip", "created_at", "id"),
        ]
