# Generated by Django 3.1.6 on 2021-02-20 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('botdata', '0029_discordguild_channel_disabled_message'),
        ('tags', '0003_auto_20210220_2117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='owners',
        ),
        migrations.AddField(
            model_name='tag',
            name='owner',
            field=models.ForeignKey(default=138751484517941259, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='botdata.discorduser'),
            preserve_default=False,
        ),
    ]
