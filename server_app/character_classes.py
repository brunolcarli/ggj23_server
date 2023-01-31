from graphene import Enum


class ChracterClass(Enum):
    DPS = 'dps'
    SUPPORTER = 'supporter'
    TANKER = 'tanker'


classes = {
    'dps': {'hp': 0, 'sp': 50, 'power': 5, 'resistance': 0, 'agility': 0},
    'supporter': {'hp': 0, 'sp': 100, 'power': 0, 'resistance': 0, 'agility': 2},
    'tanker': {'hp': 120, 'sp': 0, 'power': 0, 'resistance': 5, 'agility': 0},
}

