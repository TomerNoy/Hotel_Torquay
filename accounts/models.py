from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=300, null=True)
    phone_number = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f'{self.user.username}'
