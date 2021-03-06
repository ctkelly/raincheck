from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from datetime import date
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string

from events.models import Event, Invitation
from events.forms import EventUpdateForm, EventCreateForm, InvitationForm
from users.mail import *


class MainEventView(LoginRequiredMixin, View):
    template_name = 'events/event_list.html'

    def get(self, request, *args, **kwargs):
        today = date.today()
        el = Event.objects.filter(
            Q(owner=self.request.user) |
            Q(invitee=self.request.user),
            date__gte=today
        ).order_by('date')

        ctx = {'event_list': el}
        return render(request, 'events/event_list.html', ctx)


class EventCreateView(LoginRequiredMixin, View):
    model = Event
    template = 'events/event_form.html'
    success_url = reverse_lazy('events:all')

    def get(self, request):
        form = EventCreateForm()
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request):
        form = EventCreateForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        event = form.save(commit=False)
        event.owner = self.request.user
        event.save()

        friend1 = event.owner
        friend2 = event.invitee
        event_name = event.title
        event_date = event.date
        event_time = event.time

        # Trying a wrapper function for event created send_mass_mail
        wrapper_send_mass_mail(
            'users/event_created_email_subject.txt',
            'users/event_created_email_message.txt',
            {
                'name': friend1,
                'event_name': event_name,
                'friend': friend2,
                'event_date': event_date,
                'event_time': event_time
            },
            {
                'name': friend2,
                'event_name': event_name,
                'friend': friend1,
                'event_date': event_date,
                'event_time': event_time,
            },
            event.owner,
            event.invitee,
        )

        # Then create "invitations" for each invitee, below: THIS PART WAS MOVED TO MODEL
        # owner_invitation = Invitation(invitee=event.owner, event=event, response=True)
        # owner_invitation.save()
        # invitee_invitation = Invitation(invitee=event.invitee, event=event, response=True)
        # invitee_invitation.save()
        return redirect(self.success_url)


class InvitationUpdateView(LoginRequiredMixin, View):
    model = Invitation
    template = 'events/invitation_form.html'
    success_url = reverse_lazy('events:all')

    def get(self, request, pk):
        invitation = get_object_or_404(self.model, pk=pk)
        form = InvitationForm(instance=invitation)
        ctx = {'form': form, 'invitation': invitation}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        invitation = get_object_or_404(self.model, pk=pk)
        form = InvitationForm(request.POST, instance=invitation)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.response = False
            invitation_event = invitation.event_id
            invitation.save()

            name = request.user
            event = Event.objects.get(id=invitation_event)
            event_name = event.title
            event_date = event.date

            # Trying a wrapper function for send_mail
            wrapper_send_one_invitation_update_mail(
                'users/invitation_update_email_subject.txt',
                'users/invitation_update_email_message.txt',
                [name.email],
                {'name': name, 'event_name': event_name, 'event_date': event_date}
            )

            if Invitation.objects.filter(event_id=invitation_event, response=True).exists():
                return redirect(self.success_url)
            else:
                event = Event.objects.get(id=invitation_event)
                event.status = Event.INACTIVE
                event.save()
                friend1 = event.owner
                friend2 = event.invitee
                event_name = event.title
                event_date = event.date
                event_time = event.time

                # Trying a wrapper function for event rainchecked send_mass_mail
                wrapper_send_mass_mail(
                    'users/event_rainchecked_email_subject.txt',
                    'users/event_rainchecked_email_message.txt',
                    {
                        'name': friend1,
                        'event_name': event_name,
                        'friend': friend2,
                        'event_date': event_date,
                        'event_time': event_time
                    },
                    {
                        'name': friend2,
                        'event_name': event_name,
                        'friend': friend1,
                        'event_date': event_date,
                        'event_time': event_time,
                    },
                    event.owner,
                    event.invitee,
                )

                return redirect(self.success_url)


class EventUpdateView(LoginRequiredMixin, View):
    model = Event
    template = 'events/event_form.html'
    success_url = reverse_lazy('events:all')

    def get(self, request, pk):
        event = get_object_or_404(self.model, pk=pk)
        form = EventUpdateForm(instance=event)
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        event = get_object_or_404(self.model, pk=pk)
        form = EventUpdateForm(request.POST, instance=event)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        form.save()
        return redirect(self.success_url)


class EventDeleteView(LoginRequiredMixin, View):
    model = Event
    template = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('events:all')

    def get(self, request, pk):
        event = get_object_or_404(self.model, pk=pk)
        ctx = {'event': event}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        event = get_object_or_404(self.model, pk=pk)
        event.delete()
        return redirect(self.success_url)





