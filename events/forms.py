from django import forms
from django.forms import ModelForm
from events.models import Event, Invitation


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class InvitationForm(ModelForm):
    class Meta:
        model = Invitation
        exclude = ['invitee', 'event', 'response']


class EventUpdateForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'time']
        widgets = {
            'date': DateInput(),
            'time': TimeInput(),
            # 'time': TimeInput(format='%H:%M')
        }


class EventCreateForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'invitee', 'date', 'time']
        widgets = {
            'date': DateInput(),
            'time': TimeInput(),
        }


