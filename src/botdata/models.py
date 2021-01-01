# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import collections
import datetime
import time
import typing
from enum import unique

import pytz
from django_enumfield.enum import EnumField, Enum

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# https://www.colorschemer.com/color-picker/
DUCKS_COLORS = {
    "normal": "#55C8CE",
    "ghost": "#5294CE",
    "prof": "#4460CE",
    "baby": "#5944CE",
    "golden": "#8D42CE",
    "plastic": "#7344CE",
    "kamikaze": "#CE409F",
    "mechanical": "#CE425C",
    "super": "#CE6548",
    "moad": "#CEAE4E",
    "armored": "#9FCE46",
    "night": "#62CE44",
    "sleeping": "#4ACE97",
    "v3": "#7F8182",
    "v3_nohug": "#7F8182",
    "trees": "#0C5B00",
    "nothing": "#827B7E",
    "players": "#B8CEB8",
}

SHOP_ITEMS = ["ap_ammo", "explosive_ammo", "grease", "sight", "detector", "silencer", "clover", "sunglasses", "coat",
              "licence", "reloader", "homing_bullets"]
DUCKS_DAY_CATEGORIES = ["normal", "ghost", "prof", "baby", "golden", "plastic", "kamikaze", "mechanical", "super",
                        "moad", "armored"]
DUCKS_NIGHT_CATEGORIES = ["night", "sleeping"]


def default_dict_generator(default_factory):
    return collections.defaultdict(default_factory)


class DefaultDictJSONField(models.JSONField):
    def __init__(self, default_factory: typing.Callable = int, **kwargs: typing.Any):
        self.default_factory = default_factory
        super().__init__(**kwargs)

    def get_default(self):
        return default_dict_generator(self.default_factory)

    def to_python(self, value):
        ret = super().to_python(value)
        return collections.defaultdict(self.default_factory, ret)

    def from_db_value(self, value: str, expression, connection) -> typing.Optional[collections.defaultdict]:
        parsed = super().from_db_value(value, expression, connection)
        return collections.defaultdict(self.default_factory, parsed)


class DiscordGuild(models.Model):
    discord_id = models.BigAutoField(primary_key=True)
    first_seen = models.DateTimeField(auto_now_add=True)

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
    first_seen = models.DateTimeField(auto_now_add=True)

    guild = models.ForeignKey(DiscordGuild, models.CASCADE, related_name="channels", db_index=True)
    name = models.TextField()

    webhook_urls = models.JSONField(default=list, blank=True)
    api_key = models.UUIDField(blank=True, null=True)

    use_webhooks = models.BooleanField(default=True)
    use_emojis = models.BooleanField(default=True)
    enabled = models.BooleanField(default=False, db_index=True)

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

    def get_night_times(self):
        now = datetime.datetime.now(tz=pytz.utc)
        midnight = now.replace(microsecond=0, second=0, minute=0, hour=0)

        start_td = datetime.timedelta(seconds=self.night_start_at)
        end_td = datetime.timedelta(seconds=self.night_end_at)

        return (midnight + start_td,
                midnight + end_td)

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
    first_seen = models.DateTimeField(auto_now_add=True)


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

    first_seen = models.DateTimeField(auto_now_add=True)

    prestige = models.SmallIntegerField(default=8)
    prestige_last_daily = models.DateTimeField(auto_now_add=True)
    prestige_dailies = models.IntegerField(default=0)

    active_powerups = DefaultDictJSONField(default_factory=int)
    shooting_stats = DefaultDictJSONField(default_factory=int)

    stored_achievements = DefaultDictJSONField(default_factory=bool, blank=True)

    experience = models.BigIntegerField(default=0)
    spent_experience = models.BigIntegerField(default=0)

    givebacks = models.IntegerField(default=0)

    found_items = DefaultDictJSONField()
    bought_items = DefaultDictJSONField()

    bullets = models.IntegerField(default=6)
    magazines = models.IntegerField(default=2)

    last_giveback = models.DateTimeField(auto_now_add=True)

    weapon_sabotaged_by = models.ForeignKey('self', models.SET_NULL, blank=True, null=True)

    best_times = DefaultDictJSONField(default_factory=lambda: 660, blank=True)
    killed = DefaultDictJSONField(blank=True)
    hugged = DefaultDictJSONField(blank=True)
    hurted = DefaultDictJSONField(blank=True)
    resisted = DefaultDictJSONField(blank=True)
    frightened = DefaultDictJSONField(blank=True)

    @property
    def total_ducks_killed(self):
        return sum(self.killed.values())

    @property
    def computed_achievements(self):
        return {
            'murderer': self.shooting_stats.get('murders', 0) >= 1,
            'big_spender': self.spent_experience >= 2000,
            'first_week': self.givebacks >= 7,
            'first_month': self.givebacks >= 30,
            'first_year': self.givebacks >= 365,
            'i_dont_want_bullets': self.found_items.get('left_bullet', 0) >= 1,
            'baby_killer': self.killed.get('baby', 0) >= 5,
            'maths': self.killed.get('prof', 0) >= 5,
            'brains': self.shooting_stats.get('brains_eaten', 0) >= 5,
            'sentry_gun': self.shooting_stats.get('bullets_used', 0) >= 1000,
        }

    @property
    def achievements(self):
        return {
            **self.computed_achievements,
            **self.stored_achievements,
        }

    def sorted_killed(self):
        return dict(sorted(self.killed.items(), key=lambda e: -e[1]))

    def is_powerup_active(self, powerup):
        if self.prestige >= 1 and powerup == "sunglasses":
            return True
        elif self.prestige >= 5 and powerup == "coat":
            return True
        elif self.prestige >= 7 and powerup == "kill_licence":
            return True
        elif powerup in ["sight", "detector", "wet", "sand", "mirror", "homing_bullets", "dead", "confiscated",
                         "jammed"]:
            return self.active_powerups[powerup] > 0
        else:
            now = time.time()
            return self.active_powerups[powerup] >= now

    def get_only_active_powerups(self, only_shop_items=True):
        active = {}
        for powerup, powerup_value in self.active_powerups.items():
            if (powerup in SHOP_ITEMS or not only_shop_items) and self.is_powerup_active(powerup):
                active[powerup] = powerup_value
        return active

    def get_found_useful(self, left=False):
        dct = {}
        for item_name, item_count in self.found_items.items():
            if "trash" not in item_name:
                if (left and "left" in item_name) or (not left and "took" in item_name):
                    dct[item_name] = item_count
        return dct

    def get_found_trash(self):
        dct = {}
        for item_name, item_count in self.found_items.items():
            if "trash" in item_name:
                dct[item_name] = item_count
        return dct

    def __str__(self):
        return f"{self.member} playing on {self.channel}"

    class Meta:
        db_table = 'players'
