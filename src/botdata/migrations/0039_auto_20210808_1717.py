# Generated by Django 3.2.5 on 2021-08-08 17:17

from django.db import migrations


def move_primary_keys_from_member_to_nothing_on_landmines(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    LandminesUserData = apps.get_model('botdata', 'LandminesUserData')
    LandminesPlaced = apps.get_model('botdata', 'LandminesPlaced')

    for landmine in LandminesPlaced.objects.all():
        placed_by_id = landmine.placed_by_id
        placed_by_userdata= LandminesUserData.objects.all().get(member_id=placed_by_id)
        landmine.placed_by = placed_by_userdata

        stopped_by_id = landmine.stopped_by_id
        if stopped_by_id:
            stopped_by_userdata = LandminesUserData.objects.all().get(member_id=stopped_by_id)
            landmine.stopped_by = stopped_by_userdata

        landmine.save()


def reset_pks_to_member(apps, schema_editor):
    LandminesUserData = apps.get_model('botdata', 'LandminesUserData')
    LandminesPlaced = apps.get_model('botdata', 'LandminesPlaced')

    for landmine in LandminesPlaced.objects.all():
        placed_by_id = landmine.placed_by_id
        placed_by_userdata = LandminesUserData.objects.all().get(pk=placed_by_id)
        landmine.placed_by_id = placed_by_userdata.member_id

        stopped_by_id = landmine.stopped_by_id
        if stopped_by_id:
            stopped_by_userdata = LandminesUserData.objects.all().get(pk=stopped_by_id)

            landmine.stopped_by_id = stopped_by_userdata.member_id

        landmine.save()


class Migration(migrations.Migration):

    dependencies = [
        ('botdata', '0038_rename_newlandminesuserdata_landminesuserdata'),
    ]

    operations = [
        migrations.RunPython(move_primary_keys_from_member_to_nothing_on_landmines, reset_pks_to_member)
    ]