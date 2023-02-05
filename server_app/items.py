import uuid

from ggj23.settings import GAME_CONFIG
from server_app.events import OnCharacterEvent

item_list = {
    'mp': {
        'name': 'mp',
        'kind': 'consumable',
        'effect' : {
            'target_attributes': ['sp'],
            'duration': 0,
            'value': 0.2
        },
        'description': 'Restores 20% of the SP',
        'buy_price': 30,
        'sell_price': 20
    },
    'hp': {
        'name': 'hp',
        'kind': 'consumable',
        'effect' : {
            'target_attributes': ['hp'],
            'duration': 0,
            'value': 0.2
        },
        'description': 'Restores 20% of the HP',
        'buy_price': 30,
        'sell_price': 20
    },
    'earth_hat': {
        'name': 'earth_hat',
        'kind': 'hat',
        'effect' : None,
        'description': 'A hat of earth',
        'buy_price': 30,
        'sell_price': 20
    },
    'fire_hat': {
        'name': 'fire_hat',
        'kind': 'hat',
        'effect' : None,
        'description': 'A hat of fire',
        'buy_price': 30,
        'sell_price': 20
    },
    'air_hat': {
        'name': 'air_hat',
        'kind': 'hat',
        'effect' : None,
        'description': 'A hat of air',
        'buy_price': 30,
        'sell_price': 20
    },
    'water_hat': {
        'name': 'water_hat',
        'kind': 'hat',
        'effect' : None,
        'description': 'A hat of water',
        'buy_price': 30,
        'sell_price': 20
    },
    'light_hat': {
        'name': 'light_hat',
        'kind': 'hat',
        'effect' : None,
        'description': 'A hat of light',
        'buy_price': 30,
        'sell_price': 20
    },
    'darkness_hat': {
        'name': 'darkness_hat',
        'kind': 'hat',
        'effect' : None,
        'description': 'A hat of darkness',
        'buy_price': 30,
        'sell_price': 20
    },
    'basic_hat': {
        'name': 'basic_hat',
        'kind': 'hat',
        'effect' : None,
        'description': 'A cosmetic hat. You look good in it :)',
        'buy_price': 30,
        'sell_price': 20
    },
    'earth_staff': {
        'name': 'earth_staff',
        'kind': 'staff',
        'effect' : None,
        'description': 'A staff of earth',
        'buy_price': 30,
        'sell_price': 20
    },
    'fire_staff': {
        'name': 'fire_staff',
        'kind': 'staff',
        'effect' : None,
        'description': 'A staff of fire',
        'buy_price': 30,
        'sell_price': 20
    },
    'air_staff': {
        'name': 'air_staff',
        'kind': 'staff',
        'effect' : None,
        'description': 'A staff of air',
        'buy_price': 30,
        'sell_price': 20
    },
    'water_staff': {
        'name': 'water_staff',
        'kind': 'staff',
        'effect' : None,
        'description': 'A staff of water',
        'buy_price': 30,
        'sell_price': 20
    },
    'light_staff': {
        'name': 'light_staff',
        'kind': 'staff',
        'effect' : None,
        'description': 'A staff of light',
        'buy_price': 30,
        'sell_price': 20
    },
    'darkness_staff': {
        'name': 'darkness_staff',
        'kind': 'staff',
        'effect' : None,
        'description': 'A staff of darkness',
        'buy_price': 30,
        'sell_price': 20
    },
    'basic_staff': {
        'name': 'basic_staff',
        'kind': 'staff',
        'effect' : None,
        'description': 'A basic walking stick',
        'buy_price': 30,
        'sell_price': 20
    },
    'earth_cloak': {
        'name': 'earth_cloak',
        'kind': 'cloak',
        'effect' : None,
        'description': 'A cloak of earth',
        'buy_price': 30,
        'sell_price': 20
    },
    'fire_cloak': {
        'name': 'fire_cloak',
        'kind': 'cloak',
        'effect' : None,
        'description': 'A cloak of fire',
        'buy_price': 30,
        'sell_price': 20
    },
    'air_cloak': {
        'name': 'air_cloak',
        'kind': 'cloak',
        'effect' : None,
        'description': 'A cloak of air',
        'buy_price': 30,
        'sell_price': 20
    },
    'water_cloak': {
        'name': 'water_cloak',
        'kind': 'cloak',
        'effect' : None,
        'description': 'A cloak of water',
        'buy_price': 30,
        'sell_price': 20
    },
    'light_cloak': {
        'name': 'light_cloak',
        'kind': 'cloak',
        'effect' : None,
        'description': 'A cloak of light',
        'buy_price': 30,
        'sell_price': 20
    },
    'darkness_cloak': {
        'name': 'darkness_cloak',
        'kind': 'cloak',
        'effect' : None,
        'description': 'A cloak of darkness',
        'buy_price': 30,
        'sell_price': 20
    },
    'basic_cloak': {
        'name': 'basic_cloak',
        'kind': 'cloak',
        'effect' : None,
        'description': 'A cosmetic cloak. Doesn\'t do much, but exhales respect.',
        'buy_price': 30,
        'sell_price': 20
    },
    'earth_boots': {
        'name': 'earth_boots',
        'kind': 'boots',
        'effect' : None,
        'description': 'A boots of earth',
        'buy_price': 30,
        'sell_price': 20
    },
    'fire_boots': {
        'name': 'fire_boots',
        'kind': 'boots',
        'effect' : None,
        'description': 'A boots of fire',
        'buy_price': 30,
        'sell_price': 20
    },
    'air_boots': {
        'name': 'air_boots',
        'kind': 'boots',
        'effect' : None,
        'description': 'A boots of air',
        'buy_price': 30,
        'sell_price': 20
    },
    'water_boots': {
        'name': 'water_boots',
        'kind': 'boots',
        'effect' : None,
        'description': 'A boots of water',
        'buy_price': 30,
        'sell_price': 20
    },
    'light_boots': {
        'name': 'light_boots',
        'kind': 'boots',
        'effect' : None,
        'description': 'A boots of light',
        'buy_price': 30,
        'sell_price': 20
    },
    'darkness_boots': {
        'name': 'darkness_boots',
        'kind': 'boots',
        'effect' : None,
        'description': 'A boots of darkness',
        'buy_price': 30,
        'sell_price': 20
    },
    'basic_boots': {
        'name': 'basic_boots',
        'kind': 'boots',
        'effect' : None,
        'description': 'A cosmetic boots. You look good in it :)',
        'buy_price': 30,
        'sell_price': 20
    },
    'small_root': {
        'name': 'small_root',
        'kind': 'root',
        'effect' : None,
        'description': 'A small root of a regular tree',
        'buy_price': 30,
        'sell_price': 20
    },
    'medium_root': {
        'name': 'medium_root',
        'kind': 'root',
        'effect' : None,
        'description': 'A medium-sized root of a regular tree',
        'buy_price': 30,
        'sell_price': 20
    },
    'big_root': {
        'name': 'big_root',
        'kind': 'root',
        'effect' : None,
        'description': 'A big root of an above average tree',
        'buy_price': 30,
        'sell_price': 20
    },
    'earth_root': {
        'name': 'earth_root',
        'kind': 'root',
        'effect' : None,
        'description': 'A root of earth',
        'buy_price': 30,
        'sell_price': 20
    },
    'fire_root': {
        'name': 'fire_root',
        'kind': 'root',
        'effect' : None,
        'description': 'A root of fire',
        'buy_price': 30,
        'sell_price': 20
    },
    'air_root': {
        'name': 'air_root',
        'kind': 'root',
        'effect' : None,
        'description': 'A root of air',
        'buy_price': 30,
        'sell_price': 20
    },
    'water_root': {
        'name': 'water_root',
        'kind': 'root',
        'effect' : None,
        'description': 'A root of water',
        'buy_price': 30,
        'sell_price': 20
    },
    'light_root': {
        'name': 'light_root',
        'kind': 'root',
        'effect' : None,
        'description': 'A root of light',
        'buy_price': 30,
        'sell_price': 20
    },
    'darkness_root': {
        'name': 'darkness_root',
        'kind': 'root',
        'effect' : None,
        'description': 'A root of darkness',
        'buy_price': 30,
        'sell_price': 20
    },
    'yggdrasil_root': {
        'name': 'yggdrasil_root',
        'kind': 'root',
        'effect' : None,
        'description': 'A root of the Yggdrasil, the Sacred Tree',
        'buy_price': 30,
        'sell_price': 20
    },
    'copper_coin': {
        'name': 'copper_coin',
        'kind': 'currency',
        'effect': None,
        'description': 'A regular coin of copper',
        'value': 1
    },
    'silver_coin': {
        'name': 'silver_coin',
        'kind': 'currency',
        'effect': None,
        'description': 'A regular coin of silver. It is worth 100 copper coins',
        'value': 100
    },
    'gold_coin': {
        'name': 'gold_coin',
        'kind': 'currency',
        'effect': None,
        'description': 'A regular coin of gold. It is worth 100 silver coins',
        'value': 10000
    },
    'book_fireball': {
        'name': 'book_fireball',
        'kind': 'book',
        'effect': None,
        'description': 'A book that teaches the skill: Fireball',
        'buy_price': 30,
        'sell_price': 20
    },
    'book_eruption': {
        'name': 'book_eruption',
        'kind': 'book',
        'effect': None,
        'description': 'A book that teaches the skill: Eruption',
        'buy_price': 30,
        'sell_price': 20
    },
    'book_ice_spear': {
        'name': 'book_ice_spear',
        'kind': 'book',
        'effect': None,
        'description': 'A book that teaches the skill: Ice Spear',
        'buy_price': 30,
        'sell_price': 20
    },
    'book_ice_age': {
        'name': 'book_ice_age',
        'kind': 'book',
        'effect': None,
        'description': 'A book that teaches the skill: Ice Age',
        'buy_price': 30,
        'sell_price': 20
    },
    'book_air_cut': {
        'name': 'book_air_cut',
        'kind': 'book',
        'effect': None,
        'description': 'A book that teaches the skill: Air Cut',
        'buy_price': 30,
        'sell_price': 20
    },
    'book_storm': {
        'name': 'book_storm',
        'kind': 'book',
        'effect': None,
        'description': 'A book that teaches the skill: Storm',
        'buy_price': 30,
        'sell_price': 20
    },
    'book_stone_bullet': {
        'name': 'book_stone_bullet',
        'kind': 'book',
        'effect': None,
        'description': 'A book that teaches the skill: Stone Bullet',
        'buy_price': 30,
        'sell_price': 20
    },
    'book_meteor': {
        'name': 'book_meteor',
        'kind': 'book',
        'effect': None,
        'description': 'A book that teaches the skill: Meteor',
        'buy_price': 30,
        'sell_price': 20
    },
    'book_blindness': {
        'name': 'book_blindness',
        'kind': 'book',
        'effect': None,
        'description': 'A book that teaches the skill: Blindness',
        'buy_price': 30,
        'sell_price': 20
    },
    'book_healing': {
        'name': 'book_healing',
        'kind': 'book',
        'effect': None,
        'description': 'A book that teaches the skill: Healing',
        'buy_price': 30,
        'sell_price': 20
    },
    'book_sup_healing': {
        'name': 'book_sup_healing',
        'kind': 'book',
        'effect': None,
        'description': 'A book that teaches the skill: Superior Healing',
        'buy_price': 30,
        'sell_price': 20
    },
    'book_revive': {
        'name': 'book_revive',
        'kind': 'book',
        'effect': None,
        'description': 'A book that teaches the skill: Revive',
        'buy_price': 30,
        'sell_price': 20
    },
    'book_mana_barrier': {
        'name': 'book_mana_barrier',
        'kind': 'book',
        'effect': None,
        'description': 'A book that teaches the skill: Mana Barrier',
        'buy_price': 30,
        'sell_price': 20
    },
    'book_elemental_barrier': {
        'name': 'book_elemental_barrier',
        'kind': 'book',
        'effect': None,
        'description': 'A book that teaches the skill: Elemental Barrier',
        'buy_price': 30,
        'sell_price': 20
    },
    'book_improve_status': {
        'name': 'book_improve_status',
        'kind': 'book',
        'effect': None,
        'description': 'A book that teaches the skill: Improve Status',
        'buy_price': 30,
        'sell_price': 20
    },
    'book_enemy_casualty': {
        'name': 'book_enemy_casualty',
        'kind': 'book',
        'effect': None,
        'description': 'A book that teaches the skill: Enemy Casualty',
        'buy_price': 30,
        'sell_price': 20
    }
}


class Item:
    def __init__(self, data):
        self.id = str(uuid.uuid4())
        self.name = data['name']
        self.kind = data['kind']
        self.effect = data['effect']
        self.count = 0
        self['description'] = data['description']
        self.buy_price = data['buy_price']
        self.sell_price = data['sell_price']
        
    def use(self):
        pass        
        # TODO: self.effect.apply()
        # broadcast use item
        payload = {
            'item_name': self.name
        }
        OnCharacterEvent.char_event(params={
            'event_type': 'item_use',
            'data': payload
        })
        
def max_currency():
    return (GAME_CONFIG['MAX_GOLD_COINS']-1) * item_list['gold_coin']['value'] + (GAME_CONFIG['MAX_SILVER_COINS']-1) * item_list['silver_coin']['value'] + (GAME_CONFIG['MAX_COPPER_COINS']-1) * item_list['copper_coin']['value']