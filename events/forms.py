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


class EventCreateForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'invitee', 'date', 'time']
        widgets = {
            'date': DateInput(),  # OK -- model does not allow past dates
            'time': TimeInput(),  # OK -- time appears as 00:00 and can select AM/PM
        }


class EventUpdateForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'time']
        widgets = {
            'date': DateInput(),
            # 'time': TimeInput(),  # Makes time in update form appear as 00:00:00 instead of 00:00 (AM/PM still ok)
            'time': TimeInput(format='%H:%M'),
        }





