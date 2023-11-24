from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
# Register your models here.


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    ordering = ('id',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email', 'phone')
    list_filter = ('user', 'email', 'phone')
    search_fields = ('user', 'email', 'phone')
    ordering = ('id',)


class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('id',)

class TripInline(admin.StackedInline):
    model = Trip
    can_delete = False
    verbose_name_plural = 'trips'
    extra=0

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'driver', 'type', 'brand', 'model', 'registration', 'is_available', 'per_km', 'min_fare', 'per_day')
    list_filter = ('driver', 'type', 'brand', 'model', 'registration', 'is_available', 'per_km', 'min_fare')
    search_fields = ('driver', 'type', 'brand', 'model', 'registration', 'is_available', 'per_km', 'min_fare')
    ordering = ('id',)
    list_editable = ('is_available','per_km', 'min_fare','per_day')
    inlines = (TripInline,)


class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'vehicle', 'type', 'status', 'start_date', 'start_time', 'pickup', 'destination', 'distance', 'total_cost')
    list_filter = ('user', 'vehicle', 'type', 'status', 'start_date', 'start_time', 'pickup', 'destination', 'distance', 'total_cost')
    search_fields = ('user', 'vehicle', 'type', 'status', 'start_date', 'start_time', 'pickup', 'destination', 'distance', 'total_cost')
    ordering = ('id',)

class DriverAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'nid', 'license', 'address', 'image')
    list_filter = ('name', 'phone', 'nid', 'license', 'address')
    search_fields = ('name', 'phone', 'nid', 'license', 'address')
    ordering = ('id',)



admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(VehicleType, VehicleTypeAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(Driver, DriverAdmin)


