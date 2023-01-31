

areas = {
    'citadel': {
        'size_x': 500,
        'size_y': 500,
        'connections': ['yggdrasil', 'combat_zone', 'open_fields']
    },
    'open_fields': {
        'size_x': 500,
        'size_y': 500,
        'connections': ['citadel', 'ancient_forest_area1', 'vulcanic_zone_area1', 'snowfields_area1', 'chrono_mountains_area1']
    },
    'yggdrasil': {
        'size_x': 500,
        'size_y': 500,
        'connections': ['citadel']
    },
    'combat_zone': {
        'size_x': 500,
        'size_y': 500,
        'connections': ['citadel']
    },
    'ancient_forest_area1': {
        'size_x': 500,
        'size_y': 500,
        'connections': ['open_fields', 'ancient_forest_village']
    },
    'ancient_forest_area2': {
        'size_x': 500,
        'size_y': 500,
        'connections': ['ancient_forest_village', 'ancient_forest_area3', 'ancient_forest_elder_cave']
    },
    'ancient_forest_area3': {
        'size_x': 500,
        'size_y': 500,
        'connections': ['ancient_forest_village', 'ancient_forest_area2', 'ancient_forest_elder_cave']
    },
    'ancient_forest_elder_cave': {
        'size_x': 500,
        'size_y': 500,
        'connections': ['ancient_forest_area3', 'ancient_forest_area2']
    },
    'ancient_forest_village': {
        'size_x': 500,
        'size_y': 500,
        'connections': ['ancient_forest_area1', 'ancient_forest_area3', 'ancient_forest_area2']
    },
    'vulcanic_zone_area1': {
        'size_x': 500,
        'size_y': 500,
        'connections': []  # TODO
    },
    'vulcanic_zone_area2': {
        'size_x': 500,
        'size_y': 500,
        'connections': []  # TODO
    },
    'vulcanic_zone_area3': {
        'size_x': 500,
        'size_y': 500,
        'connections': []  # TODO
    },
    'vulcanic_zone_elder_cave': {
        'size_x': 500,
        'size_y': 500,
        'connections': []  # TODO
    },
    'vulcanic_zone_village': {
        'size_x': 500,
        'size_y': 500,
        'connections': []  # TODO
    },
    'snowfields_area1': {
        'size_x': 500,
        'size_y': 500,
        'connections': []  # TODO
    },
    'snowfields_area2': {
        'size_x': 500,
        'size_y': 500,
        'connections': []  # TODO
    },
    'snowfields_area3': {
        'size_x': 500,
        'size_y': 500,
        'connections': []  # TODO
    },
    'snowfields_elder_cave': {
        'size_x': 500,
        'size_y': 500,
        'connections': []  # TODO
    },
    'snowfields_village': {
        'size_x': 500,
        'size_y': 500,
        'connections': []  # TODO
    },
    'chrono_mountains_area1': {
        'size_x': 500,
        'size_y': 500,
        'connections': []  # TODO
    },
    'chrono_mountains_area2': {
        'size_x': 500,
        'size_y': 500,
        'connections': []  # TODO
    },
    'chrono_mountains_area3': {
        'size_x': 500,
        'size_y': 500,
        'connections': []  # TODO
    },
    'chrono_mountains_elder_cave': {
        'size_x': 500,
        'size_y': 500,
        'connections': []  # TODO
    },
    'chrono_mountains_village': {
        'size_x': 500,
        'size_y': 500,
        'connections': []  # TODO
    },
    # TODO add opne_fields subquests caves
}