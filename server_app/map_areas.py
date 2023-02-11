

areas = {
    'citadel_central_area': {
        'name': 'citadel_central_area',
        'size_x': 760,
        'size_y': 962,
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
        'connections': [
            'yggdrasil',
            'combat_zone',
            'open_fields_area8',
            'citadel_central_area'
        ]
    },
    'citadel_south_area': {
        'name': 'citadel_south_area',
        'size_x': 760,
        'size_y': 962,
        'connections': ['citadel_central_area', 'open_fields_area1']
    },
    'citadel_east_area': {
        'name': 'citadel_east_area',
        'size_x': 760,
        'size_y': 962,
        'connections': ['citadel_central_area', 'open_fields_area5']
    },
    'citadel_west_area': {
        'name': 'citadel_west_area',
        'size_x': 760,
        'size_y': 962,
        'connections': ['citadel_central_area', 'open_fields_area11']
    },
    'open_fields_area1': {
        'name': 'open_fields_area1',
        'size_x': 578,
        'size_y': 916,
        'connections': [
            'citadel_south_area',
            'open_fields_area2',
            'open_fields_area14'
            ]
    },
    'open_fields_area2': {
        'name': 'open_fields_area2',
        'size_x': 628,
        'size_y': 906,
        'connections': [
            'open_fields_area1',
            'open_fields_area3'
            ]
    },
    'open_fields_area3': {
        'name': 'open_fields_area3',
        'size_x': 576,
        'size_y': 916,
        'connections': [
            'open_fields_area2',
            'open_fields_area4'
            ]
    },
    'open_fields_area4': {
        'name': 'open_fields_area4',
        'size_x': 546,
        'size_y': 912,
        'connections': [
            'open_fields_area5',
            'open_fields_area3'
        ]
    },
    'open_fields_area5': {
        'name': 'open_fields_area5',
        'size_x': 558,
        'size_y': 914,
        'connections': [
            'open_fields_area6',
            'open_fields_area4',
            'citadel_east_area'
        ]
    },
    'open_fields_area6': {
        'name': 'open_fields_area6',
        'size_x': 578,
        'size_y': 908,
        'connections': [
            'open_fields_area7',
            'open_fields_area5'
        ]
    },
    'open_fields_area7': {
        'name': 'open_fields_area7',
        'size_x': 626,
        'size_y': 908,
        'connections': [
            'open_fields_area8',
            'open_fields_area6'
        ]
    },
    'open_fields_area8': {
        'name': 'open_fields_area8',
        'size_x': 576,
        'size_y': 888,
        'connections': [
            'open_fields_area7',
            'open_fields_area9',
            'citadel_north_area'
        ]
    },
    'open_fields_area9': {
        'name': 'open_fields_area9',
        'size_x': 576,
        'size_y': 890,
        'connections': [
            'open_fields_area8',
            'open_fields_area10'
        ]
    },
    'open_fields_area10': {
        'name': 'open_fields_area10',
        'size_x': 626,
        'size_y': 912,
        'connections': [
            'open_fields_area9',
            'open_fields_area11'
        ]
    },
    'open_fields_area11': {
        'name': 'open_fields_area11',
        'size_x': 600,
        'size_y': 910,
        'connections': [
            'open_fields_area12',
            'open_fields_area10',
            'citadel_west_area'
        ]
    },
    'open_fields_area12': {
        'name': 'open_fields_area12',
        'size_x': 600,
        'size_y': 912,
        'connections': [
            'open_fields_area13',
            'open_fields_area11'
        ]
    },
    'open_fields_area13': {
        'name': 'open_fields_area13',
        'size_x': 620,
        'size_y': 910,
        'connections': [
            'open_fields_area14',
            'open_fields_area12',
            'ancient_forest_area1'
        ]
    },
    'open_fields_area14': {
        'name': 'open_fields_area14',
        'size_x': 576,
        'size_y': 892,
        'connections': [
            'open_fields_area1',
            'open_fields_area13'
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
        'size_x': 626,
        'size_y': 726,
        'connections': ['open_fields_area13', 'ancient_forest_village']
    },
    'ancient_forest_area2': {
        'name': 'acient_forest_area2',
        'size_x': 674,
        'size_y': 1006,
        'connections': ['ancient_forest_village', 'ancient_forest_area3', 'ancient_forest_elder_cave']
    },
    'ancient_forest_area3': {
        'name': 'acient_forest_area3',
        'size_x': 672,
        'size_y': 960,
        'connections': ['ancient_forest_village', 'ancient_forest_area2', 'ancient_forest_elder_cave']
    },
    'ancient_forest_elder_cave': {
        'name': 'acient_forest_elder_cave',
        'size_x': 760,
        'size_y': 760,
        'connections': ['ancient_forest_area3', 'ancient_forest_area2']
    },
    'ancient_forest_village': {
        'name': 'acient_forest_village',
        'size_x': 656,
        'size_y': 704,
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
    'snowfields_area1': {
        'name': 'snowfields_area1',
        'size_x': 760,
        'size_y': 760,
        'connections': ['open_fields', 'snowfields_village']
    },
    'snowfields_area2': {
        'name': 'snowfields_area2',
        'size_x': 760,
        'size_y': 760,
        'connections': ['snowfields_village', 'snowfields_area3', 'snowfields_elder_cave']
    },
    'snowfields_area3': {
        'name': 'snowfields_area3',
        'size_x': 760,
        'size_y': 760,
        'connections': ['snowfields_village', 'snowfields_area2', 'snowfields_elder_cave']
    },
    'snowfields_elder_cave': {
        'name': 'snowfields_elder_cave',
        'size_x': 760,
        'size_y': 760,
        'connections': ['snowfields_area3', 'snowfields_area2']
    },
    'snowfields_village': {
        'name': 'snowfields_village',
        'size_x': 760,
        'size_y': 760,
        'connections': ['snowfields_area1', 'snowfields_area3', 'snowfields_area2']
    },
    'chrono_mountains_area1': {
        'name': 'chrono_mountains_area1',
        'size_x': 760,
        'size_y': 760,
        'connections': ['open_fields', 'chrono_mountains_village']
    },
    'chrono_mountains_area2': {
        'name': 'chrono_mountains_area2',
        'size_x': 760,
        'size_y': 760,
        'connections': ['chrono_mountains_village', 'chrono_mountains_area3', 'chrono_mountains_elder_cave']
    },
    'chrono_mountains_area3': {
        'name': 'chrono_mountains_area3',
        'size_x': 760,
        'size_y': 760,
        'connections': ['chrono_mountains_village', 'chrono_mountains_area2', 'chrono_mountains_elder_cave']
    },
    'chrono_mountains_elder_cave': {
        'name': 'chrono_mountains_elder_cave',
        'size_x': 760,
        'size_y': 760,
        'connections': ['chrono_mountains_area3', 'chrono_mountains_area2']
    },
    'chrono_mountains_village': {
        'name': 'chrono_mountains_village',
        'size_x': 760,
        'size_y': 760,
        'connections': ['chrono_mountains_area1', 'chrono_mountains_area3', 'chrono_mountains_area2']
    },
    # TODO add opne_fields subquests caves
}

area_transfer_coord_map = {
    'citadel_central_area': {
        'citadel_north_area': (300, 900),
        'citadel_south_area': (300, 16),
        'citadel_east_area': (2, 475),
        'citadel_west_area': (720, 475)
    },
    'citadel_north_area': {
        'yggdrasil': (100, 100),
        'combat_zone': (100, 100),
        'open_fields_area8': (245, 890),
        'citadel_central_area': (380, 16)
    },
    'citadel_south_area': {
        'citadel_central_area': (380, 900),
        'open_fields_area1': (300, 16)
    },
    'citadel_east_area': {
        'citadel_central_area': (720, 460),
        'open_fields_area5': (2, 500)
    },
    'citadel_west_area': {
        'citadel_central_area': (2, 470),
        'open_fields_area11': (565, 400)
    },
    'open_fields_area1': {
        'citadel_south_area': (300, 900),
        'open_fields_area2': (2, 450),
        'open_fields_area14': (580, 400)
    },
    'open_fields_area2': {
        'open_fields_area1': (580, 400),
        'open_fields_area3': (2, 458)
    },
    'open_fields_area3': {
        'open_fields_area2': (590, 450),
        'open_fields_area4': (273, 890)
    },
    'open_fields_area4': {
        'open_fields_area5': (279, 900),
        'open_fields_area3': (314, 10)
    },
    'open_fields_area5': {
        'open_fields_area6': (273, 890),
        'open_fields_area4': (273, 10),
        'citadel_east_area': (730, 470)
    },
    'open_fields_area6': {
        'open_fields_area7': (590, 450),
        'open_fields_area5': (279, 10)
    },
    'open_fields_area7': {
        'open_fields_area8': (540, 444),
        'open_fields_area6': (2, 450)
    },
    'open_fields_area8': {
        'open_fields_area7': (2, 450),
        'open_fields_area9': (569, 445),
        'citadel_north_area':(300, 16)
    },
    'open_fields_area9': {
        'open_fields_area8': (2, 444),
        'open_fields_area10': (590, 450)
    },
    'open_fields_area10': {
        'open_fields_area9': (2, 445),
        'open_fields_area11': (300, 10)
    },
    'open_fields_area11': {
        'open_fields_area12': (300, 10),
        'open_fields_area10': (305, 900),
        'citadel_west_area': (2, 470)
    },
    'open_fields_area12': {
        'open_fields_area13': (300, 16),
        'open_fields_area11': (300, 900)
    },
    'open_fields_area13': {
        'open_fields_area14': (2, 400),
        'open_fields_area12': (300, 900),
        'ancient_forest_area1': (590, 335)
    },
    'open_fields_area14': {
        'open_fields_area1': (2, 400),
        'open_fields_area13': (300, 900)
    },
    'yggdrasil': {
        'citadel_north_area': (100, 100)
    },
    'combat_zone': {
        'citadel_north_area': (100, 100)
    },
    'ancient_forest_area1': {
        'open_fields_area13': (2, 455),
        'ancient_forest_village': (620, 401)
    },
    'ancient_forest_area2': {
        'ancient_forest_village': (2, 165),
        'ancient_forest_area3': (234, 16),
        'ancient_forest_elder_cave': (100, 100)
    },
    'ancient_forest_area3': {
        'ancient_forest_village': (2, 600),
        'ancient_forest_area2': (244, 980),
        'ancient_forest_elder_cave': (100, 100)
    },
    # 'ancient_forest_elder_cave': {
    #     'name': 'acient_forest_elder_cave',
    #     'size_x': 760,
    #     'size_y': 760,
    #     'connections': ['ancient_forest_area3', 'ancient_forest_area2']
    # },
    'ancient_forest_village': {
        'ancient_forest_area1': (10, 420),
        'ancient_forest_area3': (634, 210),
        'ancient_forest_area2': (628, 740)
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
    # 'snowfields_area1': {
    #     'name': 'snowfields_area1',
    #     'size_x': 760,
    #     'size_y': 760,
    #     'connections': ['open_fields', 'snowfields_village']
    # },
    # 'snowfields_area2': {
    #     'name': 'snowfields_area2',
    #     'size_x': 760,
    #     'size_y': 760,
    #     'connections': ['snowfields_village', 'snowfields_area3', 'snowfields_elder_cave']
    # },
    # 'snowfields_area3': {
    #     'name': 'snowfields_area3',
    #     'size_x': 760,
    #     'size_y': 760,
    #     'connections': ['snowfields_village', 'snowfields_area2', 'snowfields_elder_cave']
    # },
    # 'snowfields_elder_cave': {
    #     'name': 'snowfields_elder_cave',
    #     'size_x': 760,
    #     'size_y': 760,
    #     'connections': ['snowfields_area3', 'snowfields_area2']
    # },
    # 'snowfields_village': {
    #     'name': 'snowfields_village',
    #     'size_x': 760,
    #     'size_y': 760,
    #     'connections': ['snowfields_area1', 'snowfields_area3', 'snowfields_area2']
    # },
    # 'chrono_mountains_area1': {
    #     'name': 'chrono_mountains_area1',
    #     'size_x': 760,
    #     'size_y': 760,
    #     'connections': ['open_fields', 'chrono_mountains_village']
    # },
    # 'chrono_mountains_area2': {
    #     'name': 'chrono_mountains_area2',
    #     'size_x': 760,
    #     'size_y': 760,
    #     'connections': ['chrono_mountains_village', 'chrono_mountains_area3', 'chrono_mountains_elder_cave']
    # },
    # 'chrono_mountains_area3': {
    #     'name': 'chrono_mountains_area3',
    #     'size_x': 760,
    #     'size_y': 760,
    #     'connections': ['chrono_mountains_village', 'chrono_mountains_area2', 'chrono_mountains_elder_cave']
    # },
    # 'chrono_mountains_elder_cave': {
    #     'name': 'chrono_mountains_elder_cave',
    #     'size_x': 760,
    #     'size_y': 760,
    #     'connections': ['chrono_mountains_area3', 'chrono_mountains_area2']
    # },
    # 'chrono_mountains_village': {
    #     'name': 'chrono_mountains_village',
    #     'size_x': 760,
    #     'size_y': 760,
    #     'connections': ['chrono_mountains_area1', 'chrono_mountains_area3', 'chrono_mountains_area2']
    # },
}