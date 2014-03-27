from django.test import TestCase
from login.models import User

class LoginViewTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('dan@dan.com', 'potato')
        User.objects.create_user('joe@dan.com', 'potato')

    def test_invalid_email(self):
        response = self.client.post("/login/", {'email': 'joe@da.com',
                                      'password': 'potato'}, follow=True)
        self.assertContains(response, 'The credentials were incorrect.')

    def test_invalid_pass(self):
        response = self.client.post("/login/", {'email': 'joe@dan.com',
                                      'password': 'lol'}, follow=True)
        self.assertContains(response, 'The credentials were incorrect.')

    def test_valid_login(self):
        response = self.client.post("/login/", {'email': 'joe@dan.com',
                                    'password': 'potato'}, follow=True)
        self.assertContains(response, 'Successfully logged in!')
        # We're on the profile page, user has no name:
        self.assertContains(response, 'Hello, !')

    def test_login(self):
        response = self.client.post("/login/", {'email': 'joe@dan.com',
                                      'password': 'potato'}, follow=True)
        self.assertContains(response, 'Successfully logged in!')

    def test_logout(self):
        self.client.login(email='dan@dan.com', password='potato')
        response = self.client.get("/logout/", follow=True)
        self.assertContains(response, 'Logged out.')

class RegisterViewTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('dan@dan.com', 'potato')
        User.objects.create_user('joe@dan.com', 'potato')

    def test_register_valid(self):
        c = self.client.post("/login/",
                             {'email': 'joe@dan.com',
                              'password': 'potato'}, follow=True)

