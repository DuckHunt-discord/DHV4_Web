# Generated by Django 3.2.3 on 2021-06-07 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botdata', '0015_auto_20210603_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='discordchannel',
            name='anti_trigger_wording',
            field=models.BooleanField(default=False),
        ),
    ]
