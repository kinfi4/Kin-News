from django.contrib.auth.models import User
from django.db import models


class Channel(models.Model):
    __table_name__ = 'channel'

    link = models.CharField(max_length=255, verbose_name='link')
    subscribers = models.ManyToManyField(User, related_query_name='subscriptions')

    def __str__(self):
        return self.link
