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
from django.templatetags.static import static
from django.utils import timezone
from django_enumfield.enum import EnumField, Enum

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# https://www.colorschemer.com/color-picker/
from botdata.achievements import trophys, achievements
from botdata.coats import Coats

from django.utils.translation import gettext_lazy as _

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
    "when_dead": "#827B7C",
    "duckhunt": "#2193DE"
}

SHOP_ITEMS = ["ap_ammo", "explosive_ammo", "grease", "sight", "detector", "silencer", "clover", "sunglasses", "coat",
              "licence", "reloader", "homing_bullets"]
DUCKS_DAY_CATEGORIES = ["normal", "ghost", "prof", "baby", "golden", "plastic", "kamikaze", "mechanical", "super",
                        "moad", "armored", "cartographer"]
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
    channel_disabled_message = models.BooleanField(default=True)

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

    landmines_commands_enabled = models.BooleanField(default=False)  # Can members run landmine commands here
    landmines_enabled = models.BooleanField(default=False)  # Do messages sent here count in the game ?

    allow_global_items = models.BooleanField(default=True)
    anti_trigger_wording = models.BooleanField(default=False)

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
    spawn_weight_cartographer_ducks = models.SmallIntegerField(default=3)
    ducks_time_to_live = models.SmallIntegerField(default=660)
    super_ducks_min_life = models.SmallIntegerField(default=2)
    super_ducks_max_life = models.SmallIntegerField(default=7)

    levels_to_roles_ids_mapping = models.JSONField(default=dict, blank=True)
    prestige_to_roles_ids_mapping = models.JSONField(default=dict, blank=True)

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

    __labels__ = {
        BANNED: _("Banned"),
        DEFAULT: _("Default"),
        TRUSTED: _("Trusted"),
        MODERATOR: _("Moderator"),
        ADMIN: _("Admin"),
        BOT_MODERATOR: _("Bot moderator"),
        BOT_OWNER: _("Bot owner"),
    }


class DiscordUser(models.Model):
    discord_id = models.BigAutoField(primary_key=True)
    first_seen = models.DateTimeField(auto_now_add=True)

    name = models.TextField()
    discriminator = models.CharField(max_length=4)

    trophys = models.JSONField(default=dict, blank=True)

    ping_friendly = models.BooleanField(default=True)

    language = models.CharField(max_length=6, default="en")
    first_use = models.BooleanField(default=True)

    access_level_override = EnumField(AccessLevel, default=AccessLevel.DEFAULT)

    boss_kills = models.IntegerField(default=0)

    @property
    def trophies_data(self):
        trophies_parsed = []
        for trophy_id, have in self.trophys.items():
            trophy = trophys[trophy_id]
            if have:
                trophies_parsed.append({"id": trophy_id,
                                        "image_url": static("botdata/trophies/{}.png".format(trophy_id)),
                                        "name": trophy["name"],
                                        "description": trophy["description"]})

        return trophies_parsed

    def __str__(self):
        return f"{self.name}#{self.discriminator}"

    class Meta:
        db_table = 'users'


class LandminesUserData(models.Model):
    # Ideally, member should be a OneToOneField and the primary key for the table
    # Unfortunately, https://github.com/tortoise/tortoise-orm/issues/822 wasn't fixed
    # So we have to find a workaround.
    # For that, we are just going to remove the primary_key attribute from member, and add another
    # column for the ID, but keep an index on member.
    # It might be a little slower, but at least it will work...
    member = models.OneToOneField('DiscordMember', related_name='landmines_data', on_delete=models.CASCADE, db_index=True)

    # General statistics
    first_played = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now_add=True)
    messages_sent = models.IntegerField(default=0)
    words_sent = models.IntegerField(default=0)
    points_won = models.IntegerField(default=0)        # By killing
    points_recovered = models.IntegerField(default=0)  # By defusing
    points_acquired = models.IntegerField(default=0)   # By talking
    points_current = models.IntegerField(default=0)    # Sum of everything
    points_exploded = models.IntegerField(default=0)   # By saying a bad word
    points_spent = models.IntegerField(default=0)      # By using the shop

    # Inventory

    ## Defuse kits
    defuse_kits_bought = models.IntegerField(default=0)
    shields_bought = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.member} landmines data"

    class Meta:
        db_table = 'landmines_userdata'


class LandminesPlaced(models.Model):
    placed_by = models.ForeignKey(LandminesUserData, related_name='landmines_bought', on_delete=models.CASCADE)
    placed = models.DateTimeField(auto_now_add=True)
    word = models.CharField(max_length=50)
    message = models.CharField(blank=True, default="", max_length=2000)

    value = models.IntegerField()
    exploded = models.IntegerField(null=True, blank=True)

    tripped = models.BooleanField(default=False)
    disarmed = models.BooleanField(default=False)

    stopped_by = models.ForeignKey(LandminesUserData, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='landmines_stopped')
    stopped_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.placed_by.member} landmine on {self.word} for {self.value}"

    class Meta:
        db_table = 'landmines_placed'


class LandminesProtects(models.Model):
    protected_by = models.ForeignKey(LandminesUserData, related_name='words_protected', on_delete=models.CASCADE)
    placed = models.DateTimeField(auto_now_add=True)
    protect_count = models.IntegerField(default=0)
    word = models.CharField(max_length=50)
    message = models.CharField(blank=True, default="", max_length=2000)

    def __str__(self):
        return f"{self.protected_by.member} protected word on {self.word}"

    class Meta:
        db_table = 'landmines_protected'


class UserInventory(models.Model):
    user = models.OneToOneField(DiscordUser, related_name='inventory', on_delete=models.CASCADE, primary_key=True)

    # Boxes
    lootbox_welcome_left = models.IntegerField(default=1)
    lootbox_boss_left = models.IntegerField(default=0)
    lootbox_vote_left = models.IntegerField(default=0)

    # Unobtainable items
    item_vip_card_left = models.IntegerField(default=0)

    # Loot
    item_mini_exp_boost_left = models.IntegerField(default=0)
    item_norm_exp_boost_left = models.IntegerField(default=0)
    item_maxi_exp_boost_left = models.IntegerField(default=0)
    item_one_bullet_left = models.IntegerField(default=0)
    item_spawn_ducks_left = models.IntegerField(default=0)
    item_refill_magazines_left = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} inventory"

    class Meta:
        db_table = 'inventories'


class DiscordMember(models.Model):
    access_level = EnumField(AccessLevel, default=AccessLevel.DEFAULT)

    guild = models.ForeignKey(DiscordGuild, models.CASCADE, related_name="members", db_index=True)
    user = models.ForeignKey(DiscordUser, models.CASCADE, related_name="members", db_index=True)

    def __str__(self):
        return f"{self.user} (access={self.access_level})"

    class Meta:
        db_table = 'members'


class Player(models.Model):
    channel = models.ForeignKey(DiscordChannel, models.CASCADE, related_name="players", db_index=True)
    member = models.ForeignKey(DiscordMember, models.CASCADE, db_index=True)

    first_seen = models.DateTimeField(auto_now_add=True)

    prestige = models.SmallIntegerField(default=8)
    prestige_last_daily = models.DateTimeField(auto_now_add=True)
    prestige_dailies = models.IntegerField(default=0)

    active_powerups = DefaultDictJSONField(default_factory=int)
    shooting_stats = DefaultDictJSONField(default_factory=int)

    stored_achievements = DefaultDictJSONField(default_factory=bool, blank=True)

    experience = models.BigIntegerField(default=0, db_index=True)
    spent_experience = models.BigIntegerField(default=0)

    givebacks = models.IntegerField(default=0)

    found_items = DefaultDictJSONField()
    bought_items = DefaultDictJSONField()

    bullets = models.IntegerField(default=6)
    magazines = models.IntegerField(default=2)

    last_giveback = models.DateTimeField(auto_now_add=True)

    weapon_sabotaged_by = models.ForeignKey('self', models.SET_NULL, blank=True, null=True, db_index=False)

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
            'homing_killed': self.shooting_stats.get('homing_kills', 0) >= 1,
        }

    @property
    def achievements(self):
        return {
            **self.computed_achievements,
            **self.stored_achievements,
        }

    @property
    def unlocked_achievements(self):
        l = []
        for achievement, unlocked in self.achievements.items():
            if unlocked:
                l.append(achievement)
        return l

    @property
    def achievements_data(self):
        achievements_parsed = []
        for achievement_id in self.unlocked_achievements:
            achievement = achievements[achievement_id]
            achievements_parsed.append({"id": achievement_id,
                                        "image_url": static("botdata/achievements/{}.png".format(achievement_id)),
                                        "name": achievement["name"],
                                        "description": achievement["description"]})
        return achievements_parsed

    def sorted_killed(self):
        return dict(sorted(self.killed.items(), key=lambda e: -e[1]))

    def is_powerup_active(self, powerup):
        if self.prestige >= 1 and powerup == "sunglasses":
            return True
        elif self.prestige >= 5 and powerup == "coat":
            return True
        elif self.prestige >= 7 and powerup == "kill_licence":
            return True
        elif powerup in ["coat_color", "clover_exp"]:
            return False
        elif powerup in ["sight", "detector", "sand", "mirror", "homing_bullets", "dead", "confiscated",
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

    def get_current_coat_color(self) -> typing.Optional[Coats]:
        if self.is_powerup_active('coat'):
            color_name = self.active_powerups.get('coat_color', None)
            if color_name:
                return Coats[color_name]
            else:
                # This is for older players that bought a "no_colored" coat.
                return Coats.DEFAULT
        else:
            return None

    def __str__(self):
        return f"{self.member} playing on {self.channel}"

    class Meta:
        db_table = 'players'
        constraints = [
            models.UniqueConstraint(fields=["member", "channel"], name='a_member_per_channel_only'),
        ]


class BotList(models.Model):
    # **Generic Data**
    key = models.CharField(help_text="The unique key to recognise the bot list",
                           max_length=50,
                           primary_key=True)

    name = models.CharField(help_text="Name of the bot list",
                            max_length=128)

    bot_url = models.URLField(help_text="URL for the main bot page")

    notes = models.TextField(help_text="Informations about this bot list",
                             blank=True)

    auth = models.TextField(help_text="Token used to authenticate requests to/from the bot")

    # **Votes**
    can_vote = models.BooleanField(help_text="Can people vote (more than once) on that list ?",
                                   default=True)

    vote_url = models.URLField(help_text="URL for an user to vote",
                               blank=True)

    vote_every = models.DurationField(help_text="How often can users vote ?",
                                      null=True,
                                      blank=True)

    check_vote_url = models.URLField(help_text="URL the bot can use to check if an user voted recently",
                                     blank=True)

    check_vote_key = models.CharField(help_text="Key in the returned JSON to check for presence of vote",
                                      default="voted",
                                      blank=True,
                                      max_length=128)

    check_vote_negate = models.BooleanField(
        help_text="Does the boolean says if the user has voted (True) or if he can vote (False) ?",
        default=True)

    webhook_handler = models.CharField(help_text="What is the function that'll receive the request from the vote hooks",
                                       choices=(("generic", "generic"),
                                                ("top.gg", "top.gg"),
                                                ("None", "None")),
                                       default="generic",
                                       max_length=20)

    webhook_authorization_header = models.CharField(
        help_text="Name of the header used to authenticate webhooks requests",
        default="Authorization",
        blank=True,
        max_length=20)

    webhook_user_id_json_field = models.CharField(help_text="Key that gives the user ID in the provided JSON",
                                                  default="id",
                                                  blank=True,
                                                  max_length=20)

    webhook_auth = models.TextField(
        help_text="Secret used for authentication of the webhooks messages if not the same the auth token",
        blank=True)

    # **Statistics**

    post_stats_method = models.CharField(help_text="What HTTP method should be used to send the stats",
                                         choices=(("POST", "POST"),
                                                  ("PATCH", "PATCH"),
                                                  ("None", "None")),
                                         default="POST",
                                         max_length=10)

    post_stats_url = models.URLField(help_text="Endpoint that will receive statistics",
                                     blank=True)

    post_stats_server_count_key = models.CharField(help_text="Name of the server count key in the statistics JSON",
                                                   default="server_count",
                                                   blank=True,
                                                   max_length=128)

    post_stats_shard_count_key = models.CharField(help_text="Name of the shard count key in the statistics JSON",
                                                  default="shard_count",
                                                  blank=True,
                                                  max_length=128)

    # **Others**

    bot_verified = models.BooleanField(help_text="Whether the bot was verified by the bot list staff",
                                       default=False)

    bot_certified = models.BooleanField(help_text="Whether the bot was certified on that bot list",
                                        default=False)

    embed_code = models.TextField(help_text="Code to show this bot list embed. This HTML won't be escaped.",
                                  blank=True)

    def __str__(self):
        return f"BotList {self.name}"

    class Meta:
        db_table = 'botlist'


class Vote(models.Model):
    user = models.ForeignKey(DiscordUser, models.CASCADE, related_name="votes", db_index=True)
    bot_list = models.ForeignKey(BotList, models.CASCADE, related_name="votes", db_index=True)

    at = models.DateTimeField(auto_now_add=True)
    multiplicator = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user} vote on {self.bot_list}"

    class Meta:
        db_table = 'vote'


class SupportTicket(models.Model):
    user = models.ForeignKey(DiscordUser, models.CASCADE, related_name="support_tickets", db_index=True)

    opened_at = models.DateTimeField(auto_now_add=True)

    closed = models.BooleanField(default=False)
    closed_at = models.DateTimeField(null=True, blank=True)
    closed_by = models.ForeignKey(DiscordUser, models.SET_NULL, db_index=False, null=True)
    close_reason = models.TextField(blank=True, default="")

    last_tag_used = models.ForeignKey('tags.Tag', models.SET_NULL, db_index=False, null=True)

    def opened_for(self) -> datetime.timedelta:
        if self.closed:
            td = self.closed_at - self.opened_at
        else:
            td = timezone.now() - self.opened_at

        return datetime.timedelta(seconds=int(td.total_seconds()))

    def __str__(self):
        if self.closed:
            return f"{self.user} closed ticket"
        else:
            return f"{self.user} latest ticket"

    class Meta:
        db_table = 'supportticket'
        ordering = ["-opened_at"]


class BotState(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)

    measure_interval = models.IntegerField()  # The event stats are (usually) based on a 10 minutes interval
    ws_send = models.IntegerField()
    ws_recv = models.IntegerField()
    messages = models.IntegerField()
    commands = models.IntegerField()
    command_errors = models.IntegerField()
    command_completions = models.IntegerField()

    guilds = models.IntegerField()
    users = models.IntegerField()
    shards = models.IntegerField()
    ready = models.BooleanField()
    ws_ratelimited = models.BooleanField()
    ws_latency = models.FloatField()  # miliseconds

    class Meta:
        db_table = 'botstate'
