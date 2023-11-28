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


# models for todo



class Todo(models.Model):
    todo = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.todo