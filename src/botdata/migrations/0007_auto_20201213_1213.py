# Generated by Django 3.1.4 on 2020-12-13 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('botdata', '0006_auto_20201212_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discordchannel',
            name='guild',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channels', to='botdata.discordguild'),
        ),
        migrations.AlterField(
            model_name='discordmember',
            name='guild',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='botdata.discordguild'),
        ),
        migrations.AlterField(
            model_name='discordmember',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='botdata.discorduser'),
        ),
        migrations.AlterField(
            model_name='player',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='botdata.discordchannel'),
        ),
    ]
