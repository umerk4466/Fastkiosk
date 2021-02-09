from django.contrib import admin
from .models import Category, Service, Service_booking
from .models import Event, Event_booking

from .models import Booking_status 

# Register your models here.
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Service_booking)

admin.site.register(Event)
admin.site.register(Event_booking)

admin.site.register(Booking_status)