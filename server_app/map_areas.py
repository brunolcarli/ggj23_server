

areas = {
    'citadel': {
        'name': 'citadel',
        'size_x': 760,
        'size_y': 760,
        'connections': ['yggdrasil', 'combat_zone', 'open_fields']
    },
    'open_fields': {
        'name': 'open_fields',
        'size_x': 760,
        'size_y': 760,
        'connections': ['citadel', 'ancient_forest_area1', 'vulcanic_zone_area1', 'snowfields_area1', 'chrono_mountains_area1']
    },
    'yggdrasil': {
        'name': 'yggdrasil',
        'size_x': 760,
        'size_y': 760,
        'connections': ['citadel']
    },
    'combat_zone': {
        'name': 'combat_zone',
        'size_x': 760,
        'size_y': 760,
        'connections': ['citadel']
    },
    'ancient_forest_area1': {
        'name': 'acient_forest_area1',
        'size_x': 760,
        'size_y': 760,
        'connections': ['open_fields', 'ancient_forest_village']
    },
    'ancient_forest_area2': {
        'name': 'acient_forest_area2',
        'size_x': 760,
        'size_y': 760,
        'connections': ['ancient_forest_village', 'ancient_forest_area3', 'ancient_forest_elder_cave']
    },
    'ancient_forest_area3': {
        'name': 'acient_forest_area3',
        'size_x': 760,
        'size_y': 760,
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
        'size_x': 760,
        'size_y': 760,
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