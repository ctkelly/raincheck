from django import forms
from django.forms import ModelForm
from events.models import Invitation


class InvitationForm(ModelForm):
    class Meta:
        model = Invitation
        exclude = ['invitee', 'event', 'response']


