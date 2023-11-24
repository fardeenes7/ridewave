from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings

def new_booking_email(trip):
    subject = 'New Booking Notification'
    message = f'You have a new booking for {trip.vehicle.brand} {trip.vehicle.model} from {trip.start_date} to {trip.end_date}. Please check your dashboard for details.'
    admins = User.objects.filter(is_superuser=True)
    recipients = []
    for admin in admins:
        recipients.append(admin.email)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=True)