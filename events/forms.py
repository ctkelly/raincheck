from django import forms
from django.forms import ModelForm
from events.models import Event, Invitation


class InvitationForm(ModelForm):
    class Meta:
        model = Invitation
        exclude = ['invitee', 'event', 'response']


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'time']



