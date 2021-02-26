from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group

from . mixins import TimeStampMixin


class User(AbstractUser, TimeStampMixin):
    pass


class Team(Group, TimeStampMixin):
    pass