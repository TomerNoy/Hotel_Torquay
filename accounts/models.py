from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100)
    # TEST COMMENT
    # profession = models.CharField(max_length=100)
    # address = models.CharField(max_length=100, null=True)
    # github = models.CharField(max_length=100, null=True)
    # facebook = models.CharField(max_length=100, null=True)
    # twitter = models.CharField(max_length=100, null=True)
    # instagram = models.CharField(max_length=100, null=True)
    # website = models.CharField(max_length=100, null=True)