

areas = {
    'citadel_central_area': {
        'name': 'citadel_central_area',
        'size_x': 40,
        'size_y': 40,
        'max_enemies': 0,
        'connections': [
            'citadel_north_area',
            'citadel_south_area',
            'citadel_east_area',
            'citadel_west_area'
        ]
    },
    'citadel_north_area': {
        'name': 'citadel_north_area',
        'size_x': 760,
        'size_y': 962,
        'max_enemies': 0,
        'connections': [
            'yggdrasil',
            'combat_zone',
            'open_fields_area8',
            'citadel_central_area'
        ]
    },
    'citadel_south_area': {
        'name': 'citadel_south_area',
        'size_x': 15,
        'size_y': 18,
        'max_enemies': 0,
        'connections': ['citadel_central_area', 'open_fields_area1']
    },
    'citadel_east_area': {
        'name': 'citadel_east_area',
        'size_x': 760,
        'size_y': 962,
        'max_enemies': 0,
        'connections': ['citadel_central_area', 'open_fields_area5']
    },
    'citadel_west_area': {
        'name': 'citadel_west_area',
        'size_x': 760,
        'size_y': 962,
        'max_enemies': 0,
        'connections': ['citadel_central_area', 'open_fields_area11']
    },
    'open_fields_area1': {
        'name': 'open_fields_area1',
        'size_x': 50,
        'size_y': 50,
        'max_enemies': 20,
        'connections': [
            'citadel_south_area',
            'open_fields_area2',
            'open_fields_area14'
            ]
    },
    'open_fields_area2': {
        'name': 'open_fields_area2',
        'size_x': 70,
        'size_y': 70,
        'max_enemies': 20,
        'connections': [
            'open_fields_area1',
            'open_fields_area3'
            ]
    },
    'open_fields_area3': {
        'name': 'open_fields_area3',
        'size_x': 70,
        'size_y': 70,
        'max_enemies': 16,
        'connections': [
            'open_fields_area2',
            'open_fields_area4'
            ]
    },
    'open_fields_area4': {
        'name': 'open_fields_area4',
        'size_x': 60,
        'size_y': 60,
        'max_enemies': 16,
        'connections': [
            'open_fields_area5',
            'open_fields_area3'
        ]
    },
    'open_fields_area5': {
        'name': 'open_fields_area5',
        'size_x': 60,
        'size_y': 65,
        'max_enemies': 16,
        'connections': [
            'open_fields_area6',
            'open_fields_area4',
            'citadel_east_area'
        ]
    },
    'open_fields_area6': {
        'name': 'open_fields_area6',
        'size_x': 70,
        'size_y': 70,
        'max_enemies': 16,
        'connections': [
            'open_fields_area7',
            'open_fields_area5'
        ]
    },
    'open_fields_area7': {
        'name': 'open_fields_area7',
        'size_x': 70,
        'size_y': 70,
        'max_enemies': 16,
        'connections': [
            'open_fields_area8',
            'open_fields_area6'
        ]
    },
    'open_fields_area8': {
        'name': 'open_fields_area8',
        'size_x': 70,
        'size_y': 70,
        'max_enemies': 16,
        'connections': [
            'open_fields_area7',
            'open_fields_area9',
            'snow_fields_area1'
        ]
    },
    'open_fields_area9': {
        'name': 'open_fields_area9',
        'size_x': 70,
        'size_y': 58,
        'max_enemies': 16,
        'connections': [
            'open_fields_area8',
            'open_fields_area10'
        ]
    },
    'open_fields_area10': {
        'name': 'open_fields_area10',
        'size_x': 60,
        'size_y': 80,
        'max_enemies': 16,
        'connections': [
            'open_fields_area9',
            'open_fields_area11'
        ]
    },
    'open_fields_area11': {
        'name': 'open_fields_area11',
        'size_x': 50,
        'size_y': 68,
        'max_enemies': 30,
        'connections': [
            'open_fields_area12',
            'open_fields_area10',
            'open_fields_area14',
            'citadel_west_area'
        ]
    },
    'open_fields_area12': {
        'name': 'open_fields_area12',
        'size_x': 60,
        'size_y': 80,
        'max_enemies': 60,
        'connections': [
            'open_fields_area13',
            'open_fields_area11',
            'chrono_mountains_area1',
        ]
    },
    'open_fields_area13': {
        'name': 'open_fields_area13',
        'size_x': 25,
        'size_y': 35,
        'max_enemies': 22,
        'connections': [
            'open_fields_area14',
            'open_fields_area12',
            'ancient_forest_area1'
        ]
    },
    'open_fields_area14': {
        'name': 'open_fields_area14',
        'size_x': 30,
        'size_y': 50,
        'max_enemies': 22,
        'connections': [
            'open_fields_area1',
            'open_fields_area13',
            'open_fields_area11',
        ]
    },
    'yggdrasil': {
        'name': 'yggdrasil',
        'size_x': 760,
        'size_y': 760,
        'connections': ['citadel_north_area']
    },
    'combat_zone': {
        'name': 'combat_zone',
        'size_x': 760,
        'size_y': 760,
        'connections': ['citadel_north_area']
    },
    'ancient_forest_area1': {
        'name': 'acient_forest_area1',
        'size_x': 40,
        'size_y': 40,
        'max_enemies': 16,
        'connections': ['open_fields_area13', 'ancient_forest_village']
    },
    'ancient_forest_area2': {
        'name': 'acient_forest_area2',
        'size_x': 40,
        'size_y': 40,
        'max_enemies': 16,
        'connections': ['ancient_forest_village', 'ancient_forest_area3', 'ancient_forest_dungeon']
    },
    'ancient_forest_area3': {
        'name': 'acient_forest_area3',
        'size_x': 40,
        'size_y': 40,
        'max_enemies': 16,
        'connections': ['ancient_forest_village', 'ancient_forest_area2', 'ancient_forest_dungeon']
    },
    'ancient_forest_dungeon': {
        'name': 'ancient_forest_dungeon',
        'size_x': 150,
        'size_y': 150,
        'max_enemies': 80,
        'connections': ['ancient_forest_area3', 'ancient_forest_area2']
    },
    'ancient_forest_village': {
        'name': 'acient_forest_village',
        'size_x': 28,
        'size_y': 28,
        'max_enemies': 0,
        'connections': ['ancient_forest_area1', 'ancient_forest_area3', 'ancient_forest_area2']
    },
    'vulcanic_zone_area1': {
        'name': 'vulcanic_zone_area1',
        'size_x': 760,
        'size_y': 760,
        'connections': ['open_fields', 'vulcanic_zone_village']
    },
    'vulcanic_zone_area2': {
        'name': 'vulcanic_zone_area2',
        'size_x': 760,
        'size_y': 760,
        'connections': ['vulcanic_zone_village', 'vulcanic_zone_area3', 'vulcanic_zone_elder_cave']
    },
    'vulcanic_zone_area3': {
        'name': 'vulcanic_zone_area3',
        'size_x': 760,
        'size_y': 760,
        'connections': ['vulcanic_zone_village', 'vulcanic_zone_area2', 'vulcanic_zone_elder_cave']
    },
    'vulcanic_zone_elder_cave': {
        'name': 'vulcanic_zone_elder_cave',
        'size_x': 760,
        'size_y': 760,
        'connections': ['vulcanic_zone_area3', 'vulcanic_zone_area2']
    },
    'vulcanic_zone_village': {
        'name': 'vulcanic_zone_village',
        'size_x': 760,
        'size_y': 760,
        'connections': ['vulcanic_zone_area1', 'vulcanic_zone_area3', 'vulcanic_zone_area2']
    },
    'snow_fields_area1': {
        'name': 'snow_fields_area1',
        'size_x': 100,
        'size_y': 100,
        'max_enemies': 50,
        'connections': ['open_fields_area8', 'snow_fields_area2']
    },
    'snow_fields_area2': {
        'name': 'snow_fields_area2',
        'size_x': 60,
        'size_y': 60,
        'max_enemies': 26,
        'connections': ['snow_fields_village', 'snow_fields_area1']
    },
    # 'snow_fields_area3': {
    #     'name': 'snow_fields_area3',
    #     'size_x': 50,
    #     'size_y': 50,
    #     'max_enemies': 26,
    #     'connections': ['snow_fields_village', 'snow_fields_dungeon']
    # },
    # 'snow_fields_dungeon': {
    #     'name': 'snowfields_elder_cave',
    #     'size_x': 760,
    #     'size_y': 760,
    #     'connections': ['snowfields_area3', 'snowfields_area2']
    # },
    # 'snow_fields_village': {
    #     'name': 'snowfields_village',
    #     'size_x': 760,
    #     'size_y': 760,
    #     'connections': ['snowfields_area1', 'snowfields_area3', 'snowfields_area2']
    # },
    'chrono_mountains_area1': {
        'name': 'chrono_mountains_area1',
        'size_x': 60,
        'size_y': 60,
        'max_enemies': 16,
        'connections': ['open_fields_area12', 'chrono_mountains_area2']
    },
    'chrono_mountains_area2': {
        'name': 'chrono_mountains_area2',
        'size_x': 58,
        'size_y': 80,
        'max_enemies': 50,
        'connections': ['chrono_mountains_village', 'chrono_mountains_area1']
    },
    'chrono_mountains_area3': {
        'name': 'chrono_mountains_area3',
        'size_x': 50,
        'size_y': 70,
        'max_enemies': 60,
        'connections': ['chrono_mountains_village', 'chrono_mountains_dungeon']
    },
    'chrono_mountains_dungeon': {
        'name': 'chrono_mountains_dungeon',
        'size_x': 200,
        'size_y': 200,
        'max_enemies': 250,
        'connections': ['chrono_mountains_area3']
    },
    'chrono_mountains_village': {
        'name': 'chrono_mountains_village',
        'size_x': 40,
        'size_y': 40,
        'max_enemies': 0,
        'connections': ['chrono_mountains_area2', 'chrono_mountains_area3']
    },
}

area_transfer_coord_map = {
    'citadel_central_area': {
        'citadel_north_area': (300, 900),
        'citadel_south_area': (7, 1),
        'citadel_east_area': (48, 475),
        'citadel_west_area': (720, 475)
    },
    'citadel_north_area': {
        'yggdrasil': (100, 100),
        'combat_zone': (100, 100),
        'open_fields_area8': (245, 890),
        'citadel_central_area': (380, 48)
    },
    'citadel_south_area': {
        'citadel_central_area': (20, 38),
        'open_fields_area1': (22, 2)
    },
    'citadel_east_area': {
        'citadel_central_area': (720, 460),
        'open_fields_area5': (48, 500)
    },
    'citadel_west_area': {
        'citadel_central_area': (48, 470),
        'open_fields_area11': (565, 400)
    },
    'open_fields_area1': {
        'citadel_south_area': (7, 16),
        'open_fields_area2': (48, 450),
        'open_fields_area14': (28, 19)
    },
    'open_fields_area2': {
        'open_fields_area1': (580, 400),
        'open_fields_area3': (48, 458)
    },
    'open_fields_area3': {
        'open_fields_area2': (590, 450),
        'open_fields_area4': (273, 890)
    },
    'open_fields_area4': {
        'open_fields_area5': (279, 900),
        'open_fields_area3': (314, 48)
    },
    'open_fields_area5': {
        'open_fields_area6': (273, 890),
        'open_fields_area4': (273, 48),
        'citadel_east_area': (730, 470)
    },
    'open_fields_area6': {
        'open_fields_area7': (590, 450),
        'open_fields_area5': (279, 48)
    },
    'open_fields_area7': {
        'open_fields_area8': (540, 444),
        'open_fields_area6': (48, 450)
    },
    'open_fields_area8': {
        'open_fields_area7': (48, 450),
        'open_fields_area9': (68, 53),
        'snow_fields_area1': (1, 89)
    },
    'open_fields_area9': {
        'open_fields_area8': (1, 50),
        'open_fields_area10': (57, 17),
        'citadel_north_area':(300, 48)
    },
    'open_fields_area10': {
        'open_fields_area9': (1, 54),
        'open_fields_area11': (34, 2)
    },
    'open_fields_area11': {
        'open_fields_area12': (58, 13),
        'open_fields_area10': (44, 78),
        'open_fields_area14': (22, 1),
        'citadel_west_area': (48, 470)
    },
    'open_fields_area12': {
        'open_fields_area13': (10, 4),
        'open_fields_area11': (1, 12),
        'chrono_mountains_area1': (6, 55),
    },
    'open_fields_area13': {
        'open_fields_area14': (1, 19),
        'open_fields_area12': (53, 75),
        'ancient_forest_area1': (38, 20)
    },
    'open_fields_area14': {
        'open_fields_area1': (1, 19),
        'open_fields_area13': (23, 19),
        'open_fields_area11': (41, 66)
    },
    'yggdrasil': {
        'citadel_north_area': (100, 100)
    },
    'combat_zone': {
        'citadel_north_area': (100, 100)
    },
    'ancient_forest_area1': {
        'open_fields_area13': (1, 21),
        'ancient_forest_village': (26, 15)
    },
    'ancient_forest_area2': {
        'ancient_forest_village': (1, 4),
        'ancient_forest_area3': (7, 1),
        'ancient_forest_dungeon': (148, 57)
    },
    'ancient_forest_area3': {
        'ancient_forest_village': (1, 24),
        'ancient_forest_area2': (8, 38),
        'ancient_forest_dungeon': (148, 142)
    },
    'ancient_forest_dungeon': {
        'ancient_forest_area3': (1, 30),
        'ancient_forest_area2': (1, 5)
    },
    'ancient_forest_village': {
        'ancient_forest_area1': (1, 11),
        'ancient_forest_area3': (38, 27),
        'ancient_forest_area2': (38, 32)
    },
    # 'vulcanic_zone_area1': {
    #     'name': 'vulcanic_zone_area1',
    #     'size_x': 760,
    #     'size_y': 760,
    #     'connections': ['open_fields', 'vulcanic_zone_village']
    # },
    # 'vulcanic_zone_area2': {
    #     'name': 'vulcanic_zone_area2',
    #     'size_x': 760,
    #     'size_y': 760,
    #     'connections': ['vulcanic_zone_village', 'vulcanic_zone_area3', 'vulcanic_zone_elder_cave']
    # },
    # 'vulcanic_zone_area3': {
    #     'name': 'vulcanic_zone_area3',
    #     'size_x': 760,
    #     'size_y': 760,
    #     'connections': ['vulcanic_zone_village', 'vulcanic_zone_area2', 'vulcanic_zone_elder_cave']
    # },
    # 'vulcanic_zone_elder_cave': {
    #     'name': 'vulcanic_zone_elder_cave',
    #     'size_x': 760,
    #     'size_y': 760,
    #     'connections': ['vulcanic_zone_area3', 'vulcanic_zone_area2']
    # },
    # 'vulcanic_zone_village': {
    #     'name': 'vulcanic_zone_village',
    #     'size_x': 760,
    #     'size_y': 760,
    #     'connections': ['vulcanic_zone_area1', 'vulcanic_zone_area3', 'vulcanic_zone_area2']
    # },
    'snow_fields_area1': {
        'open_fields_area8': (68, 8),
        'snow_fields_area2': (22, 57),
    },
    'snow_fields_area2': {
        'snow_fields_area1': (2, 1),
        'snow_fields_village': (44, 78),
    },
    'snow_fields_area3': {
        'snow_fields_village': (58, 13),
        'snow_fields_dungeon': (44, 78),
    },
    'snow_fields_dungeon': {
        'snow_fields_area3': (58, 13),
    },
    'snow_fields_village': {
        'snow_fields_area2': (58, 13),
        'snow_fields_area3': (44, 78),
    },
    'chrono_mountains_area1': {
        'open_fields_area12': (7, 15),
        'chrono_mountains_area2': (9, 78),
    },
    'chrono_mountains_area2': {
        'chrono_mountains_area1': (52, 37),
        'chrono_mountains_village': (16, 38),
    },
    'chrono_mountains_area3': {
        'chrono_mountains_dungeon': (21, 197),
        'chrono_mountains_village': (38, 7),
    },
    'chrono_mountains_dungeon': {
        'chrono_mountains_area3': (40, 5),
    },
    'chrono_mountains_village': {
        'chrono_mountains_area2': (11, 2),
        'chrono_mountains_area3': (1, 27),
    },
}