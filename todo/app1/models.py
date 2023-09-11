from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=10,
        
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Phone number must be a 10-digit number.'
            )
        ]
    )
