from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User


class TestMainEventView(TestCase):

    def setUp(self):
        self.url = reverse('events:all')
        self.user = User(username='testuser')
        self.user.save()

    def test_login_required(self):
        response = self.client.get(self.url)
        redirect_url = "{}?next={}".format(settings.LOGIN_URL, self.url)
        # self.assertEqual(response.status_code, 302)  # Check that the first thing equals the second thing
        self.assertRedirects(response, redirect_url)

    def test_logged_in_user_can_access(self):  # This is assuming the person is already logged in
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
