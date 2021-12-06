import os
import random

import django
from datetime import datetime, timedelta
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hotel_Torquay.settings')
django.setup()

from staff.models import *
from django.contrib.auth.models import User

fake = Faker()

# create rooms

single = RoomType.objects.create(name='single')
double = RoomType.objects.create(name='double')
suite = RoomType.objects.create(name='suite')

for i in range(5):
    Room.objects.create(room_type=single, price=200)
for i in range(5):
    Room.objects.create(room_type=double, price=300)
for i in range(3):
    Room.objects.create(room_type=suite, price=700)

# create clients
for i in range(20):
    first_name = fake.first_name()
    last_name = fake.last_name()
    pwd = fake.password(length=12)

    user = User.objects.create(
        username=first_name + str(random.randint(0, 100)),
        first_name=first_name,
        last_name=last_name,
        email=fake.email(),
        password=pwd,
    )

    Profile.objects.create(
        user=user,
        address=fake.address(),
        phone_number=fake.phone_number()
    )

# create staff

for i in range(10):
    first_name = fake.first_name()
    last_name = fake.last_name()
    pwd = fake.password(length=12)

    user = User.objects.create(
        username=first_name + last_name,
        first_name=first_name,
        last_name=last_name,
        email=fake.email(),
        password=pwd,
        is_staff=True
    )

    Profile.objects.create(
        user=user,
        address=fake.address(),
        phone_number=fake.phone_number()
    )

# create bookings (20 tries, some might not be avail)
for i in range(20):
    check_in = fake.future_date()
    # check out is random between after 1 day and after 1 week
    min_check_out = check_in + timedelta(days=1)
    max_check_out = check_in + timedelta(days=random.randint(1, 7))
    check_out = fake.date_between_dates(min_check_out, max_check_out)

    # random room
    room = random.choice(Room.objects.all()),
    room = room[0]

    # check if room avail
    room_bookings = Booking.objects.filter(room_id=room.id)

    print('wanted dates', room, check_in, check_out)
    print('room_bookings', room_bookings)

    is_avail = True

    for booking in room_bookings:
        #  check if booking dats overlap
        diff1 = (booking.check_in - check_out).days  # negative means check_out is after booking.check_in
        diff2 = (check_in - booking.check_out).days  # negative means check_in is before booking.check_out

        if diff1 < 0 and diff2 < 0:
            is_avail = False

    if is_avail:
        Booking.objects.create(
            guest=random.choice(Profile.objects.all()),
            room=room,
            check_in=check_in,
            check_out=check_out,
        )
    else:
        print('unavail')
