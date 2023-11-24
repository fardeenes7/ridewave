from django.urls import path
from .views import *
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

    path('vehicles/', vehicle_list, name='vehicle_list'),
    path('vehicles/<int:pk>/', vehicle_detail, name='vehicle_detail'),
    path('vehicles/<int:pk>/booking/', booking, name='vehicle_booking'),
    path('vehicles/<int:pk>/booking/status', booking_status, name='booking_status'),

    path('login/', login, name='login'),
    path('register/', register, name='register'),

    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('user/profile/', profile, name='profile'),
    path('user/logout/', logout, name='logout'),
    path('user/trips/', trip_list, name='trip_list'),
    path('user/trips/<int:pk>/', trip_detail, name='trip_detail'),
    path('user/trips/<int:pk>/cancel', trip_cancel, name='trip_cancel'),

    path('api/trips/', api_trip_list, name='api_trip_list'),
]