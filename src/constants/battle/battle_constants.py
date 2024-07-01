from enum import Enum


class BattleType(Enum):
    GROUND_AB = "ground-ab"
    AIR_AB = "air-ab"
    SEA_AB = "sea-ab"
    GROUND_RB = "ground-rb"
    AIR_RB = "air-rb"
    SEA_RB = "sea-rb"


class Faction(Enum):
    US = "us"
    GER = "germany"
    USSR = "ussr"
    GBR = "britain"
    JPN = "japan"
    CN = "china"
    ITLY = "italy"
    FR = "france"
    SE = "sweden"
    ISRL = "israel"
