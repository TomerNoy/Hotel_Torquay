from django.contrib import admin
from .models import *

admin.site.register(Message)
admin.site.register(Review)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Booking)

