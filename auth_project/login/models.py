from django.db import models

# Create your models here.
class User(AbstractBaseUser):
    email = models.CharField(max_length=70, unique=True, db_index=True)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    web_url = models.CharField(max_length=70)
    is_verified = models.BooleanField()
    
    USERNAME_FIELD = 'identifier'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']