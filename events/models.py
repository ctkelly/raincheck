from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime, date, timedelta
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

# Don't need this now because same day events not allowed
# def validate_time(time):
#     if time < datetime.now().time():
#         raise ValidationError('Event time cannot be in the past.')


class Event(models.Model):

    ACTIVE = 1
    INACTIVE = 0

    title = models.CharField(max_length=100, blank=False)
    invitee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_invitee')
    date = models.DateField(
        auto_now=False,
        auto_now_add=False,
        blank=False,
        validators=[MinValueValidator(date.today() + timedelta(days=1))],  # Event must be +1 day in the future
    )
    time = models.TimeField(
        auto_now=False,
        auto_now_add=False,
        blank=False,
        # validators=[validate_time],
    )
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

    # Create the invitations within the model
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
        )
        if not Invitation.objects.filter(invitee=self.owner, event=self).exists():
            owner_invitation = Invitation(invitee=self.owner, event=self, response=True)
            owner_invitation.save()
        if not Invitation.objects.filter(invitee=self.invitee, event=self).exists():
            invitee_invitation = Invitation(invitee=self.invitee, event=self, response=True)
            invitee_invitation.save()


class Invitation(models.Model):
    invitee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    response = models.BooleanField(default=True)

    def __str__(self):
        # return "{}'s {} Invitation".format(self.invitee.username, self.event.title)
        # Same thing with f-strings, below:
        return f"{self.invitee.username}'s {self.event.title} Invitation"

    @property
    def invitation_status(self):
        # If response is True (the default):
        if self.response:
            return "My status: I'm attending!"
        elif self.event.status == Event.INACTIVE:
            return ""
        else:
            return "My status: Requested a raincheck..."







