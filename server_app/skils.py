

skill_list = {
    'base_attack': {
        'sp_cost': 0,
        'power': 10,
        'range': 1,
        'effect': None,
        'classes': ['dps', 'supporter', 'tanker'],
        'description': 'Basic offensice attack',
    },
    'fireball': {
        'sp_cost':10,
        'power': 30,
        'range': 3,
        'effect': None,
        'classes': ['dps'],
        'description': 'Shots a fireball against the enemy',
    },
    'eruption': {
        'sp_cost': 18,
        'power': 50,
        'range': 5,
        'effect': None,
        'classes': ['dps'],
        'description': 'Use power of nature to pump a flow of melted rocks from undergroud',
    },
    'ice_lance': {
        'sp_cost': 20,
        'power': 60,
        'range': 3,
        'effect': None,
        'classes': ['dps'],
        'description': 'Throw a frozen spike against an enemy',
    },
    'glacial': {
        'sp_cost': 26,
        'power': 80,
        'range': 5,
        'effect': None,
        'classes': ['dps'],
        'description': 'Cast an violent blizzard around the enemy',
    },
    'air_cutter': {
        'sp_cost': 10,
        'power': 15,
        'range': 2,
        'effect': None,
        'classes': ['dps', 'supporter'],
        'description': 'Shots an fast windblow towards the enemy',
    },
    'windstorm': {
        'sp_cost': 10,
        'power': 50,
        'range': 4,
        'effect': None,
        'classes': ['dps', 'supporter'],
        'description': 'Summon a furious hurricane around the enemy',
    },
    'rock_throw': {
        'sp_cost': 15,
        'power': 40,
        'range': 2,
        'effect': None,
        'classes': ['dps', 'tanker'],
        'description': 'Shots a fierce rock blast towards an enemy',
    },
    'meteor': {
        'sp_cost': 80,
        'power': 150,
        'range': 8,
        'effect': None,
        'classes': ['dps'],
        'description': 'Summons a devastating meteor from the skies above an enemy',
    },
    'blind': {
        'sp_cost': 10,
        'power': 0,
        'range': 10,
        'effect': {
            'target_attributes': ['aim'],
            'duration': 2,
            'value': .25
        },
        'classes': ['supporter'],
        'description': 'Reduce the enemy aim in 25% for 2 minutes',
    },
    'cure': {
        'sp_cost': 20,
        'power': 0,
        'range': 6,
        'effect': {
            'target_attributes': ['hp'],
            'duration': 0,
            'value': .30
        },
    'classes': ['supporter', 'tanker'],
    'description': 'Restores up to 30% from target max HP',
    },
    'super_cure': {
        'sp_cost': 50,
        'power': 0,
        'range': 6,
        'effect': {
            'target_attributes': ['hp'],
            'duration': 0,
            'value': .60
        },
        'classes':['supporter'],
        'description': 'Restores up to 60% from target max HP',
    },
    'revive': {
        'sp_cost': 100,
        'power': 0,
        'range': 2,
        'effect': {
            'target_attributes': ['hp'],
            'duration': 0,
            'value': .50,
            'condition': 'is_ko'
        },
        'classes': ['supporter', 'tanker'],
        'description': 'Revives a fallen target with up to 50% max HP',
    },
    'mana_barrier': {
        'sp_cost': 25,
        'power': 0,
        'range': 0,
        'effect': {
            'target_attributes': ['resistance'],
            'duration': 3,
            'value': .35
        },
        'classes': ['tanker'],
        'description': 'Increases self resistance in 35% for 3 minutes',
    },
    'elemental_barrier': {
        'sp_cost': 30,
        'power': 0,
        'range': 5,
        'effect': {
            'target_attributes': ['resistance'],
            'duration': 2,
            'value': .20
        },
        'classes': ['supporter', 'tanker'],
        'description': 'Increases a target player resistance in 20% for 2 minutes',
    },
    'status_up': {
        'sp_cost': 60,
        'power': 0,
        'range': 6,
        'effect': {
            'target_attributes': ['power', 'resistance'],
            'duration': 2,
            'value': .10
        },
        'classes': ['supporter'],
        'description': 'Increases a target player power and resistance in 10% for 2 minutes',
    },
    'enemy_down': {
        'sp_cost': 20,
        'power': 0,
        'range': 5,
        'effect': {
            'target_attributes': ['power', 'resistance'],
            'duration': 2,
            'value': -.10
        },
        'classes': ['supporter'],
        'description': 'Reduce an enemy power and resistance in 10% for 2 minutes',
    },
}