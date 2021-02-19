from enum import Enum, unique


@unique
class Coats(Enum):
    DEFAULT    = "Blank", \
                 "A useful coat when it rains."

    ORANGE     = "Orange", \
                 "Better visibility: Increase your chance to frighten ducks, and reduce your chance to get shot by another hunter."

    CAMO       = "Camo", \
                 "Lower visibility: Less chance to frighten ducks."

    BLUE       = "Blue", \
                 "Lucky find: Increase your chance to find items in bushes."

    RED        = "Red", \
                 "Hungry for blood: Increase your murder skills, reduce murder penalties."

    YELLOW     = "Yellow", \
                 "Sun powers: Mirrors are less effective against you."

    DARK_GREEN = "Dark green", \
                 "Farming skills: Clovers give you one more experience point."

    BLACK      = "Black", \
                 "Secret service: Sabotages are cheaper."

    # LMAO this is useless
    LIGHT_BLUE = "Light blue", \
                 "Sea powers: You are immune to water buckets."

    PINK       = "Pink", \
                 "Power of love: You can't kill players with the same coat color."