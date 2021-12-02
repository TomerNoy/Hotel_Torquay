import os
import django

# from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hotel_Torquay.settings')
django.setup()

from visitors.models import *
from django.contrib.auth.models import User

# f = Faker()
