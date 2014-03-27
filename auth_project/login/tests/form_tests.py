from django.test import TestCase
from login.forms import LoginForm


class LoginFormTestCase(TestCase):
    def create_form(self, email='', password=''):
        return LoginForm(data={'email': email, 'password': password})

    # test_all_valid
    # test_all_valid_at_borders:
    # test_invalid_for_each_field
    # test_invalid_above_borders

    def test_login(self):
        f = self.create_form('dan', 'potato')
        self.assertFalse(f.is_valid())

        f = self.create_form('dan@gmail.com', '')
        self.assertFalse(f.is_valid())
