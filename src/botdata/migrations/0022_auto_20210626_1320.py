# Generated by Django 3.2.4 on 2021-06-26 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('botdata', '0021_auto_20210611_1023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event2021userdata',
            name='electricity_in_inventory',
        ),
        migrations.RemoveField(
            model_name='event2021userdata',
            name='found_times',
        ),
        migrations.RemoveField(
            model_name='event2021userdata',
            name='gloves_bought',
        ),
        migrations.RemoveField(
            model_name='event2021userdata',
            name='gloves_in_inventory',
        ),
        migrations.RemoveField(
            model_name='event2021userdata',
            name='landmines_in_inventory',
        ),
        migrations.RemoveField(
            model_name='event2021userdata',
            name='points_found',
        ),
        migrations.RemoveField(
            model_name='event2021userdata',
            name='points_shocked',
        ),
        migrations.RemoveField(
            model_name='event2021userdata',
            name='safes_in_inventory',
        ),
        migrations.RemoveField(
            model_name='event2021userdata',
            name='shocked_times',
        ),
        migrations.RemoveField(
            model_name='event2021userdata',
            name='shocks_prevented',
        ),
    ]
