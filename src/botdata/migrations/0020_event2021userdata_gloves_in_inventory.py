# Generated by Django 3.2.4 on 2021-06-11 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botdata', '0019_event2021landmines_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='event2021userdata',
            name='gloves_in_inventory',
            field=models.IntegerField(default=0),
        ),
    ]
