from django.db import models
from django.contrib.auth.models import User
from math import ceil
from .emails import *
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', null=True, on_delete=models.CASCADE)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=11)

    def __str__(self):
        return self.user.get_full_name() if self.user.first_name else self.user.username
    
    def name(self):
        return self.user.get_full_name() if self.user.first_name else self.user.username
    
    def save(self, *args, **kwargs):
        if not self.email:
            self.email = self.user.email
        else:
            self.user.email = self.email
        self.user.save()
        super(Profile, self).save(*args, **kwargs)
    

class Driver(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=200, null=True, blank=True)
    nid = models.CharField(max_length=17)
    license = models.CharField(max_length=20)
    address = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/driver/')

    def __str__(self):
        return self.name


class VehicleType(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    

class Vehicle(models.Model):
    driver = models.ForeignKey(Driver, null=True, on_delete=models.SET_NULL)
    type = models.ForeignKey(VehicleType, related_name='vehicles', null=True, on_delete=models.SET_NULL)
    brand = models.CharField(max_length=50, null=True)
    model = models.CharField(max_length=50)
    seats = models.IntegerField()
    registration = models.CharField(max_length=10)
    color = models.CharField(max_length=10)
    image = models.ImageField(null=True, blank=True, upload_to='images/vehicle/')
    is_available = models.BooleanField(default=True)
    per_km = models.FloatField()
    min_fare = models.FloatField(default=2000)
    per_day = models.FloatField(default=8000)

    def __str__(self):
        return self.brand + ' ' + self.model
    


class Trip(models.Model):
    TRIP_TYPE = (
        ('One Way', 'One Way'),
        ('Round Trip', 'Round Trip'),
        ('Body Rent', 'Body Rent'),
    )
    STATUS = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, related_name='trips',  null=True, on_delete=models.SET_NULL)
    driver = models.ForeignKey(Driver, related_name='trips', null=True, blank=True, on_delete=models.SET_NULL)
    vehicle = models.ForeignKey(Vehicle, related_name='trips', null=True, on_delete=models.SET_NULL)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TRIP_TYPE, default='One Way')
    pickup = models.CharField(max_length=200)
    destination = models.CharField(max_length=200, null=True, blank=True)
    distance = models.CharField(max_length=20, null=True, blank=True)
    days = models.IntegerField(null=True, blank=True)
    total_cost = models.FloatField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS, default='Pending')
    def __str__(self):
        return str(self.user) + ' - ' + str(self.driver) + ' - ' + str(self.vehicle)
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            super(Trip, self).save(*args, **kwargs)
            new_booking_email(self)
        else:
            super(Trip, self).save(*args, **kwargs)

    def calculate_cost(self):
        if self.type == 'One Way':
            self.total_cost = self.vehicle.per_km * self.distance
        elif self.type == 'Round Trip':
            self.total_cost = self.vehicle.per_km * self.distance * 2
        elif self.type == 'Body Rent':
            self.total_cost = (self.vehicle.per_day * self.days) + 700


class Review(models.Model):
    trip = models.ForeignKey(Trip, related_name='reviews', null=True, on_delete=models.SET_NULL)
    comment = models.CharField(max_length=200, null=True)
    rating = models.IntegerField(null=True)

    def __str__(self):
        return str(self.user) + ' - ' + str(self.driver) + ' - ' + str(self.vehicle)
    

