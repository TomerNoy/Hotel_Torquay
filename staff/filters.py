import django_filters

from staff.models import *


class BookingFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Booking
        fields = [
            'guest',
            'room__room_type',
            'check_in',
            'check_out',
        ]

