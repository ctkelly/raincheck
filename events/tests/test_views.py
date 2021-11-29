from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.contrib.auth.models import User
from events.models import Event, Invitation
from datetime import datetime, timedelta

# NEED TO ADD INVITATION UPDATE VIEW TEST


class BaseEventViewTestCase(TestCase):
    url = None

    def setUp(self):
        self.user = User(username='testuser')
        self.user.save()
        self.invitee = User(username='invitee')
        self.invitee.save()
        self.today = datetime.now()


class TestMainEventView(BaseEventViewTestCase):
    url = reverse_lazy('events:all')

    def test_login_required(self):
        response = self.client.get(self.url)
        redirect_url = "{}?next={}".format(settings.LOGIN_URL, self.url)
        # self.assertEqual(response.status_code, 302)  # Check that the first thing equals the second thing...
        # ...but better to check the specific url as below
        self.assertRedirects(response, redirect_url)

    def test_logged_in_user_can_access(self):  # This is assuming the person is already logged in
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    # Check that same day events retrieved (if time > now), future events retrieved, past events not retrieved
    def test_same_day_and_future_events_retrieved_but_no_past_events(self):

        event_time_today = self.today + timedelta(hours=1)
        tomorrow = self.today + timedelta(days=1)
        yesterday = self.today - timedelta(days=1)

        self.client.force_login(self.user)

        # Event 1: set the date to today but the time to one hour in the future
        self.event1 = Event(
            title='Event1',
            invitee=self.invitee,
            date=self.today,
            time=event_time_today,
            owner=self.user,
        )
        self.event1.save()

        # Event 2: set the date and time to tomorrow (24 hrs into the future)
        self.event2 = Event(
            title='Event2',
            invitee=self.invitee,
            date=tomorrow,
            time=tomorrow.time(),
            owner=self.user,
        )
        self.event2.save()

        # Event 3: set the date and time to yesterday (24 hours ago)
        self.event3 = Event(
            title='Event3',
            invitee=self.invitee,
            date=yesterday,
            time=yesterday.time(),
            owner=self.user,
        )
        self.event3.save()

        response = self.client.get(reverse('events:all'))

        # Check that there are events in the event_list
        self.assertTrue(response.context['event_list'].count() > 0)

        for event in response.context['event_list']:
            # Make a datetime object for each event and check it's > datetime.now()
            dt = datetime(event.date.year, event.date.month, event.date.day, event.time.hour, event.time.minute)
            self.assertTrue(dt > datetime.now())


class TestEventCreateView(BaseEventViewTestCase):
    url = reverse_lazy('events:event_create')

    # Check that EventCreateView creates an event and the invitations for owner and invitee
    def test_event_is_created_and_invitations_are_created(self):

        tomorrow = self.today + timedelta(days=1)

        self.client.force_login(self.user)
        self.assertEqual(Event.objects.count(), 0)

        # Simulate a user creating an event from the form
        data = {
            'title': 'Event1',
            'invitee': str(self.invitee.id),
            'date': str(tomorrow.date()),
            'time': str(tomorrow.time()),
            'owner': str(self.user.id),
        }

        self.client.post(self.url, data=data)

        event = Event.objects.get(owner=self.user)
        invitation1 = Invitation.objects.get(invitee=self.user)
        invitation2 = Invitation.objects.get(invitee=self.invitee)

        self.assertEqual(event.title, 'Event1')
        self.assertEqual(event.invitee, self.invitee)
        self.assertEqual(event.date, tomorrow.date())
        self.assertEqual(event.time, tomorrow.time())
        self.assertEqual(event.owner, self.user)
        self.assertEqual(invitation1.invitee, self.user)
        self.assertEqual(invitation1.event_id, event.id)
        self.assertEqual(invitation1.response, True)
        self.assertEqual(invitation2.invitee, self.invitee)
        self.assertEqual(invitation2.event_id, event.id)
        self.assertEqual(invitation2.response, True)


class TestEventUpdateView(BaseEventViewTestCase):
    # NO CAN'T DO THE BELOW -- because the event doesn't exist yet
    # url = reverse_lazy('events:event_update', kwargs={'pk': self.event.id})

    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        tomorrow = self.today + timedelta(days=1)

        # Creating an event in the database so I can test the UpdateView
        self.event = Event.objects.create(
            title='Event1',
            invitee=self.invitee,
            date=tomorrow,
            time=tomorrow.time(),
            owner=self.user,
        )

        self.url = reverse('events:event_update', kwargs={'pk': self.event.id})

    def test_event_is_updated(self):
        # A paranoia check that the setUp() worked
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(self.event.title, 'Event1')

        # Update the event
        next_week = self.today + timedelta(days=7)

        response = self.client.post(
            self.url, {
                'title': 'NewEventName',
                'invitee': str(self.invitee.id),
                'date': str(next_week.date()),
                'time': str(next_week.time()),
                'owner': str(self.user.id),
            }
        )

        # Check that it redirects to the correct page after POST
        self.assertRedirects(response, reverse('events:all'))

        self.event.refresh_from_db()

        self.assertEqual(self.event.title, 'NewEventName')
        self.assertEqual(self.event.date, next_week.date())
        self.assertEqual(self.event.time, next_week.time())


class TestEventDeleteView(BaseEventViewTestCase):

    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        tomorrow = self.today + timedelta(days=1)

        # Creating an event in the database so I can test the DeleteView
        self.event = Event.objects.create(
            title='Event1',
            invitee=self.invitee,
            date=tomorrow,
            time=tomorrow.time(),
            owner=self.user,
        )

        self.url = reverse('events:event_delete', kwargs={'pk': self.event.id})

    def test_event_is_deleted(self):
        # A paranoia check that the setUp() worked
        event = Event.objects.filter(pk=self.event.id)
        self.assertTrue(event.exists())
        # The below is not as precise
        # self.assertEqual(Event.objects.count(), 1)
        # self.assertEqual(self.event.title, 'Event1')

        response = self.client.post(self.url)

        # self.event.refresh_from_db()  # This is not needed?

        # Check that event was deleted
        self.assertFalse(event.exists())
        # The below is not as precise
        # self.assertEqual(Event.objects.count(), 0)
        # Check that redirects to correct page after POST
        self.assertRedirects(response, reverse('events:all'))


class TestInvitationUpdateView(BaseEventViewTestCase):

    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        tomorrow = self.today + timedelta(days=1)

        # Simulate a user creating an event from the form
        data = {
            'title': 'Event1',
            'invitee': str(self.invitee.id),
            'date': str(tomorrow.date()),
            'time': str(tomorrow.time()),
            'owner': str(self.user.id),
        }

        self.client.post(reverse('events:event_create'), data=data)

    def test_invitation_is_updated(self):
        event = Event.objects.get(owner=self.user)
        self.assertEqual(event.title, 'Event1')

        invitation1 = Invitation.objects.get(invitee=self.user)
        self.url = reverse('events:invitation_update', kwargs={'pk': event.id})
        response = self.client.post(self.url)
        invitation1.refresh_from_db()
        self.assertFalse(invitation1.response)
        self.assertRedirects(response, reverse('events:all'))











