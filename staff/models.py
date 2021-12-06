from django.db import models

from accounts.models import Profile


class Message(models.Model):
    full_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=100)
    message = models.CharField(max_length=500)
    username = models.CharField(max_length=30, null=True, blank=True)


class Review(models.Model):
    guest = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=500)


class RoomType(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Room(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=2)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)

    def __str__(self):
        return f'room ID {self.pk}'


class Booking(models.Model):
    guest = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='guest')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField(null=True)
    check_out = models.DateField(null=True)

    def __str__(self):
        return f'{self.guest} {self.room} {self.check_in} - {self.check_out}'
