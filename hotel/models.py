from django.db import models
from django.utils import timezone
# from .accounts import Profile FIX once Profile Class is defined inside accounts/models
# from decimal import Decimal

# Create your models here.


class RoomType(models.Model):
    TypeAvailable = models.TextChoices('TypeAvailable', 'doubleRoom suite patioSuite')


class Room(models.Model):
    nameType = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)


class Booking(models.Model):
    # clientId = models.ForeignKey(Profile, on_delete=models.CASCADE)
    roomId = models.ForeignKey(Room, on_delete=models.CASCADE)
    enterDate = models.DateTimeField(null=True)
    leaveDate = models.DateTimeField(null=True)
    roomType = models.ForeignKey(RoomType, on_delete=models.CASCADE)


class Review(models.Model):
    # clientId = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
