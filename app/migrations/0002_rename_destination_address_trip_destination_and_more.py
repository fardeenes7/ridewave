# Generated by Django 4.2.4 on 2023-08-12 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='destination_address',
            new_name='destination',
        ),
        migrations.RenameField(
            model_name='trip',
            old_name='pickup_address',
            new_name='pickup',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='vehicle_color',
            new_name='color',
        ),
    ]
