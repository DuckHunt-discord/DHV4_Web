# Generated by Django 3.1.4 on 2021-01-01 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botdata', '0010_auto_20201230_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discordchannel',
            name='enabled',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]