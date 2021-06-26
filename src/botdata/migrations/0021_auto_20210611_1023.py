# Generated by Django 3.2.4 on 2021-06-11 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botdata', '0020_event2021userdata_gloves_in_inventory'),
    ]

    operations = [
        migrations.AddField(
            model_name='event2021userdata',
            name='found_times',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event2021userdata',
            name='gloves_bought',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event2021userdata',
            name='points_found',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event2021userdata',
            name='points_shocked',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event2021userdata',
            name='shocked_times',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event2021userdata',
            name='shocks_prevented',
            field=models.IntegerField(default=0),
        ),
    ]