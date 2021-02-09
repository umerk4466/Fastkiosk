from django.db import models
from django.contrib.auth.models import User

# booking table
class Booking_status(models.Model):
    status = models.CharField(max_length=225, unique=True)

    def __str__(self):
        return self.status

# service tables.
class Category(models.Model):
    name = models.CharField(max_length=225, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name 

class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=225, unique=True)
    description = models.TextField()
    service_city = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    image_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Service_booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_approver = models.ForeignKey(User, null=True, blank=True,on_delete=models.SET_NULL, related_name='service_approver')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.ForeignKey(Booking_status, null=True, on_delete=models.SET_NULL)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status.status

# events tables 

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    image_url = models.URLField(null=True, blank=True)
    event_date = models.DateField()
    event_start_time = models.TimeField()
    event_finish_time = models.TimeField()
    event_address = models.CharField(max_length=255)
    event_city = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Event_booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    event_approver = models.ForeignKey(User, null=True, blank=True,on_delete=models.SET_NULL, related_name='event_approver')
    status = models.ForeignKey(Booking_status, null=True, on_delete=models.SET_NULL)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status.status