from django.db import models
from django.contrib.auth.models import User


class IP(models.Model):
    value = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=20)
    first_seen = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    feed_name = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class Hash(models.Model):
    value = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=20)
    first_seen = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    feed_name = models.CharField(max_length=100)

    def __str__(self):
        return self.type

