# Generated by Django 3.2.5 on 2021-07-31 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('botdata', '0022_auto_20210626_1320'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Event2021Landmines',
            new_name='LandminesPlaced',
        ),
        migrations.RenameModel(
            old_name='Event2021UserData',
            new_name='LandminesUserData',
        ),
    ]