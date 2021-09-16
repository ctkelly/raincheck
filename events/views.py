from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from events.models import Event


class MainEventView(LoginRequiredMixin, View):
    # This view currently shows the events that the user has created -- BUT NOT ANYONE ELSE'S events.
    # This is good.  But now need to also show events that the user has been invited to,
    # but hasn't created themselves.
    def get(self, request):
        el = Event.objects.filter(owner=self.request.user)
        ctx = {'event_list': el}
        return render(request, 'events/event_list.html', ctx)


class EventCreateView(LoginRequiredMixin, CreateView):
    # This view should also create another instance of an event for invitee(s)?
    model = Event
    fields = ['title', 'date', 'time']
    success_url = reverse_lazy('events:all')

    def form_valid(self, form):
        object = form.save(commit=False)  # Do I need to change this variable name?
        object.owner = self.request.user
        object.save()
        return super(EventCreateView, self).form_valid(form)


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['title', 'date', 'time']
    success_url = reverse_lazy('events:all')

    def get_queryset(self):
        qs = super(EventUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    fields = ['title', 'date', 'time']
    success_url = reverse_lazy('events:all')

    def get_queryset(self):
        qs = super(EventDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)

