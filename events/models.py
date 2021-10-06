from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Event(models.Model):
    ACTIVE = 1
    INACTIVE = 0

    title = models.CharField(max_length=100, blank=False)
    invitee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_invitee')
    date = models.DateField(auto_now=False, auto_now_add=False, blank=False)
    time = models.TimeField(auto_now=False, auto_now_add=False, blank=False)
    status = models.IntegerField(default=ACTIVE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_owner')

    def __str__(self):
        return self.title

    @property  # Adding @property allows us to call display_status without ()  def get_display_status
    def display_status(self):  # A noun. A computed property. Just checks, returns, doesn't do anything.
        if self.status == self.ACTIVE:
            return "It's on!"
        else:
            return "Raincheck granted!"


class Invitation(models.Model):
    invitee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    response = models.BooleanField(default=True)

    def __str__(self):
        return "{}'s {} Invitation".format(self.invitee.username, self.event.title)

    @property
    def invitation_status(self):
        if self.response:
            return "I'm attending!"
        else:
            return "Requested a raincheck..."









