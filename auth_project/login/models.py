from django.db import models
from django.contrib.auth.models import \
    AbstractBaseUser,\
           BaseUserManager,\
           PermissionsMixin, \
           UserManager
from django.core.mail import send_mail
from django.utils import timezone

import random
import string


def generate_code(length=30):
    # letter sequence of length 30: 3.5e-43 chance of collision
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


class EmailUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        email = UserManager.normalize_email(email)
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        user = self.model(email=email, is_staff=False,
                          is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    web_url = models.URLField()
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    pw_reset_code = models.CharField(null=True, max_length=30)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = EmailUserManager()

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def recover_pass(self):
        """ Generate and send end e-mail with password recovery code """
        email = self.email
        code = generate_code()
        send_mail('Reset password', 'Hi, dear %s!\n' % self.get_short_name()
                  + 'The code is: ' + code, 'no-reply@auth.com',
                  [email], fail_silently=False)

        self.pw_reset_code = code
        self.save()

    def verify(self):
        self.is_verified = True
        self.save()
