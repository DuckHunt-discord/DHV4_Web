# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import collections
import typing
from enum import unique

from django_enumfield.enum import EnumField, Enum

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


def default_dict_generator(default_factory):
    return collections.defaultdict(default_factory)


class DefaultDictJSONField(models.JSONField):
    def __init__(self, default_factory: typing.Callable = int, **kwargs: typing.Dict):
        self.default_factory = default_factory
        super().__init__(**kwargs)

    def get_default(self):
        return default_dict_generator(self.default_factory)

    def to_python(self, value):
        ret = super().to_python(value)
        return collections.defaultdict(self.default_factory, ret)

    def from_db_value(self, value: typing.Optional[collections.defaultdict], **kwargs) -> typing.Optional[str]:
        value = dict(value)
        return super().from_db_value(value, **kwargs)


class DiscordGuild(models.Model):
    discord_id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    prefix = models.CharField(max_length=20, blank=True, null=True)
    vip = models.BooleanField(default=False)
    language = models.CharField(max_length=6, default="en")

    def __str__(self):
        return f"{self.name} ({self.discord_id})"

    class Meta:
        db_table = 'guilds'


class DiscordChannel(models.Model):
    discord_id = models.BigAutoField(primary_key=True)

    guild = models.ForeignKey(DiscordGuild, models.CASCADE, related_name="channels")
    name = models.TextField()

    webhook_urls = models.JSONField(default=list, blank=True)
    api_key = models.UUIDField(blank=True, null=True)

    use_webhooks = models.BooleanField(default=True)
    use_emojis = models.BooleanField(default=True)
    enabled = models.BooleanField(default=False)

    allow_global_items = models.BooleanField(default=True)

    tax_on_user_send = models.SmallIntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(100)])
    mentions_when_killed = models.BooleanField(default=True)
    show_duck_lives = models.BooleanField(default=True)

    kill_on_miss_chance = models.SmallIntegerField(default=3)
    duck_frighten_chance = models.SmallIntegerField(default=7)

    clover_min_experience = models.SmallIntegerField(default=1)
    clover_max_experience = models.SmallIntegerField(default=10)

    base_duck_exp = models.SmallIntegerField(default=10)
    per_life_exp = models.SmallIntegerField(default=7)

    ducks_per_day = models.SmallIntegerField(default=96)

    night_start_at = models.IntegerField(default=0)
    night_end_at = models.IntegerField(default=0)

    spawn_weight_normal_ducks = models.SmallIntegerField(default=100)
    spawn_weight_super_ducks = models.SmallIntegerField(default=15)
    spawn_weight_baby_ducks = models.SmallIntegerField(default=7)
    spawn_weight_prof_ducks = models.SmallIntegerField(default=10)
    spawn_weight_ghost_ducks = models.SmallIntegerField(default=1)
    spawn_weight_moad_ducks = models.SmallIntegerField(default=5)
    spawn_weight_mechanical_ducks = models.SmallIntegerField(default=1)
    spawn_weight_armored_ducks = models.SmallIntegerField(default=3)
    spawn_weight_golden_ducks = models.SmallIntegerField(default=1)
    spawn_weight_plastic_ducks = models.SmallIntegerField(default=6)
    spawn_weight_kamikaze_ducks = models.SmallIntegerField(default=6)
    spawn_weight_night_ducks = models.SmallIntegerField(default=100)
    spawn_weight_sleeping_ducks = models.SmallIntegerField(default=5)
    ducks_time_to_live = models.SmallIntegerField(default=660)
    super_ducks_min_life = models.SmallIntegerField(default=2)
    super_ducks_max_life = models.SmallIntegerField(default=7)

    def __str__(self):
        return f"#{self.name}"

    class Meta:
        db_table = 'channels'


@unique
class AccessLevel(Enum):
    BANNED = 0
    DEFAULT = 50
    TRUSTED = 100
    MODERATOR = 200
    ADMIN = 300
    BOT_MODERATOR = 500
    BOT_OWNER = 600


class DiscordUser(models.Model):
    discord_id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    discriminator = models.CharField(max_length=4)
    times_ran_example_command = models.IntegerField(default=0)

    inventory = models.JSONField(default=list, blank=True)
    trophys = models.JSONField(default=dict, blank=True)

    ping_friendly = models.BooleanField(default=True)

    language = models.CharField(max_length=6, default="en")
    first_use = models.BooleanField(default=True)

    access_level_override = EnumField(AccessLevel, default=AccessLevel.DEFAULT)

    def __str__(self):
        return f"{self.name}#{self.discriminator}"

    class Meta:
        db_table = 'users'


class DiscordMember(models.Model):
    access_level = EnumField(AccessLevel, default=AccessLevel.DEFAULT)

    guild = models.ForeignKey(DiscordGuild, models.CASCADE, related_name="members")
    user = models.ForeignKey(DiscordUser, models.CASCADE, related_name="members")

    def __str__(self):
        return f"{self.user} (access={self.access_level})"

    class Meta:
        db_table = 'members'


class Player(models.Model):
    channel = models.ForeignKey(DiscordChannel, models.CASCADE, related_name="players")
    member = models.ForeignKey(DiscordMember, models.CASCADE)

    prestige = models.SmallIntegerField(default=8)
    prestige_last_daily = models.DateTimeField(auto_now_add=True)
    prestige_dailies = models.IntegerField(default=0)

    active_powerups = DefaultDictJSONField(default_factory=int)
    shooting_stats = DefaultDictJSONField(default_factory=int)

    stored_achievements = DefaultDictJSONField(default_factory=bool)

    experience = models.BigIntegerField(default=0)
    spent_experience = models.BigIntegerField(default=0)

    givebacks = models.IntegerField(default=0)

    found_items = DefaultDictJSONField()
    bought_items = DefaultDictJSONField()

    bullets = models.IntegerField(default=6)
    magazines = models.IntegerField(default=2)

    last_giveback = models.DateTimeField(auto_now_add=True)

    weapon_sabotaged_by = models.ForeignKey('self', models.SET_NULL, blank=True, null=True)

    best_times = DefaultDictJSONField(default_factory=lambda: 660)
    killed = DefaultDictJSONField()
    hugged = DefaultDictJSONField()
    hurted = DefaultDictJSONField()
    resisted = DefaultDictJSONField()
    frightened = DefaultDictJSONField()

    def __str__(self):
        return f"{self.member} playing on {self.channel}"

    class Meta:
        db_table = 'players'
