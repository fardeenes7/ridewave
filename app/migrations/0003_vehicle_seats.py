# Generated by Django 4.2.4 on 2023-08-12 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_destination_address_trip_destination_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='seats',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
