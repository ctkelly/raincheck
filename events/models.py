from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Status(models.Model):
    class Meta:
        verbose_name_plural = 'status'

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=100, blank=False)
    date = models.DateField(auto_now=False, auto_now_add=False, blank=False)
    time = models.TimeField(auto_now=False, auto_now_add=False, blank=False)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title




