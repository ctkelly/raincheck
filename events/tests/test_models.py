from django.test import TestCase
from django.contrib.auth.models import User
from events.models import Event, Invitation
from datetime import datetime, timedelta
from django.urls import reverse, reverse_lazy


class EventModelTest(TestCase):

    def setUp(self):

        self.user = User(username='testuser')
        self.user.save()
        self.invitee = User(username='invitee')
        self.invitee.save()

        self.today = datetime.now()
        tomorrow = self.today + timedelta(days=1)

        # Creating an event in the database so I can test the methods
        self.event = Event.objects.create(
            title='Event1',
            invitee=self.invitee,
            date=tomorrow,
            time=tomorrow.time(),
            owner=self.user,
        )

    # Check that event's string representation is equal to its title(?)
    def test_title_is_string(self):
        self.assertEqual(str(self.event), self.event.title)

    def test_display_status(self):
        # ACTIVE and INACTIVE are attributes that are tied to the class, not a particular instance
        self.event.status = Event.ACTIVE
        self.assertEqual(self.event.display_status, "It's on!")
        self.event.status = Event.INACTIVE
        self.assertEqual(self.event.display_status, "Raincheck granted!")


class InvitationModelTest(TestCase):

    def setUp(self):
        self.user = User(username='testuser')
        self.user.save()
        self.invitee = User(username='invitee')
        self.invitee.save()
        self.today = datetime.now()
        tomorrow = self.today + timedelta(days=1)
        self.url = reverse('events:event_create')
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

        # NO we are not testing the views
        self.client.post(self.url, data=data)

    def test_invitation_string_representation_is_correct_in_admin(self):

        event = Event.objects.get(owner=self.user)
        invitation1 = Invitation.objects.get(invitee=self.user)
        invitation2 = Invitation.objects.get(invitee=self.invitee)

        owner_invitation_name = f"{self.user}'s {event.title} Invitation"
        invitee_invitation_name = f"{self.invitee}'s {event.title} Invitation"

        self.assertEqual(str(invitation1), owner_invitation_name)
        self.assertEqual(str(invitation2), invitee_invitation_name)

    def test_that_invitation_responses_initially_set_to_true(self):
        # Create the invitations in here

        invitation1 = Invitation.objects.get(invitee=self.user)
        invitation2 = Invitation.objects.get(invitee=self.invitee)

        self.assertTrue(invitation1.response)
        self.assertTrue(invitation2.response)

    def test_invitation_status_message_is_correct(self):

        initial_msg = "My status: I'm attending!"
        raincheck_msg = "My status: Requested a raincheck..."
        raincheck_granted = ""
        event = Event.objects.get(owner=self.user)
        invitation1 = Invitation.objects.get(invitee=self.user)
        invitation2 = Invitation.objects.get(invitee=self.invitee)

        self.assertEqual(invitation1.invitation_status, initial_msg)
        self.assertEqual(invitation2.invitation_status, initial_msg)

        invitation1.response = False
        invitation1.save()
        self.assertEqual(invitation1.invitation_status, raincheck_msg)
        invitation2.response = False
        invitation2.save()
        self.assertEqual(invitation2.invitation_status, raincheck_msg)

        event.status = Event.INACTIVE
        event.save()

        # event.refresh_from_db()
        invitation1.refresh_from_db()
        invitation2.refresh_from_db()

        self.assertEqual(invitation1.invitation_status, raincheck_granted)
        self.assertEqual(invitation2.invitation_status, raincheck_granted)








