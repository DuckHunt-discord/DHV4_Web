# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Aerich(models.Model):
    version = models.CharField(max_length=255)
    app = models.CharField(max_length=20)
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'aerich'


class Channels(models.Model):
    discord_id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    webhook_urls = models.JSONField()
    api_key = models.UUIDField(blank=True, null=True)
    use_webhooks = models.BooleanField()
    use_emojis = models.BooleanField()
    enabled = models.BooleanField()
    allow_global_items = models.BooleanField()
    tax_on_user_send = models.SmallIntegerField()
    mentions_when_killed = models.BooleanField()
    show_duck_lives = models.BooleanField()
    kill_on_miss_chance = models.SmallIntegerField()
    duck_frighten_chance = models.SmallIntegerField()
    clover_min_experience = models.SmallIntegerField()
    clover_max_experience = models.SmallIntegerField()
    base_duck_exp = models.SmallIntegerField()
    per_life_exp = models.SmallIntegerField()
    ducks_per_day = models.SmallIntegerField()
    night_start_at = models.IntegerField()
    night_end_at = models.IntegerField()
    spawn_weight_normal_ducks = models.SmallIntegerField()
    spawn_weight_super_ducks = models.SmallIntegerField()
    spawn_weight_baby_ducks = models.SmallIntegerField()
    spawn_weight_prof_ducks = models.SmallIntegerField()
    spawn_weight_ghost_ducks = models.SmallIntegerField()
    spawn_weight_moad_ducks = models.SmallIntegerField()
    spawn_weight_mechanical_ducks = models.SmallIntegerField()
    spawn_weight_armored_ducks = models.SmallIntegerField()
    spawn_weight_golden_ducks = models.SmallIntegerField()
    spawn_weight_plastic_ducks = models.SmallIntegerField()
    spawn_weight_kamikaze_ducks = models.SmallIntegerField()
    spawn_weight_night_ducks = models.SmallIntegerField()
    spawn_weight_sleeping_ducks = models.SmallIntegerField()
    ducks_time_to_live = models.SmallIntegerField()
    super_ducks_min_life = models.SmallIntegerField()
    super_ducks_max_life = models.SmallIntegerField()
    guild = models.ForeignKey('Guilds', models.DO_NOTHING)

    class Meta:
        db_table = 'channels'


class Guilds(models.Model):
    discord_id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    prefix = models.CharField(max_length=20, blank=True, null=True)
    vip = models.BooleanField()
    language = models.CharField(max_length=6)

    class Meta:
        db_table = 'guilds'


class Members(models.Model):
    access_level = models.SmallIntegerField()
    guild = models.ForeignKey(Guilds, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        db_table = 'members'


class Players(models.Model):
    prestige = models.SmallIntegerField()
    prestige_last_daily = models.DateTimeField()
    prestige_dailies = models.IntegerField()
    active_powerups = models.JSONField()
    shooting_stats = models.JSONField()
    stored_achievements = models.JSONField()
    experience = models.BigIntegerField()
    spent_experience = models.BigIntegerField()
    givebacks = models.IntegerField()
    found_items = models.JSONField()
    bought_items = models.JSONField()
    bullets = models.IntegerField()
    magazines = models.IntegerField()
    last_giveback = models.DateTimeField()
    best_times = models.JSONField()
    killed = models.JSONField()
    hugged = models.JSONField()
    hurted = models.JSONField()
    resisted = models.JSONField()
    frightened = models.JSONField()
    weapon_sabotaged_by = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    channel = models.ForeignKey(Channels, models.DO_NOTHING)
    member = models.ForeignKey(Members, models.DO_NOTHING)

    class Meta:
        db_table = 'players'


class Users(models.Model):
    discord_id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    discriminator = models.CharField(max_length=4)
    times_ran_example_command = models.IntegerField()
    inventory = models.JSONField()
    trophys = models.JSONField()
    ping_friendly = models.BooleanField()
    language = models.CharField(max_length=6)
    first_use = models.BooleanField()
    access_level_override = models.SmallIntegerField()

    class Meta:
        db_table = 'users'