from enum import IntEnum

class __GameEnum(IntEnum):
    @classmethod
    def get(cls, member:str):
        if len(list(filter(str.isupper, member))) >= 2 and '_' not in member:
            for _member in cls.__members__:
                if _member.upper().replace("_", "") == member.upper():
                    return cls[_member]
        else:
            return cls[member.upper()]

class MasteryCodes(__GameEnum):
    NONE = 0
    GLOVE = 1
    TONFA = 2
    BAT = 3
    WHIP = 4
    HIGH_ANGLE_FIRE = 5
    DIRECT_FIRE = 6
    BOW = 7
    CROSS_BOW = 8
    PISTOL = 9
    ASSAULT_RIFLE = 10
    SNIPER_RIFLE = 11
    HAMMER = 13
    AXE = 14
    ONE_HAND_SWORD = 15
    TWO_HAND_SWORD = 16
    POLEARM = 17
    DUAL_SWORD = 18
    SPEAR = 19
    NUNCHAKU = 20
    RAPIER = 21
    GUITAR = 22
    CAMERA = 23
    ARCANA = 24
    VF_ARM = 25

    CRAFT = 101
    SEARCH = 102
    MOVE = 103

    DEFENCE = 201
    HUNT = 202
    MEDITATION = 203

    # Deleted
    #TRAP = None
    #HEALTH = None

class ServerCodes(__GameEnum):
    ASIA = 10
    NORTH_AMERICA = 12
    EUROPE = 13
    SOUTH_AMERICA = 14
    ASIA2 = 17

class MatchingTeamModes(__GameEnum):
    SOLO = 0
    DUO = 1
    SQUAD = 2

class MatchingModes(__GameEnum):
    NORMAL = 2
    RANKED = 3
    COBALT = 6

class EqupmentCodes(__GameEnum):
    WEAPON = 0
    CHEST = 1
    HEAD = 2
    ARM = 3
    LEG = 4
    TRINKET = 5