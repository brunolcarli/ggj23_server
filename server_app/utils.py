

class CharacterPublishPayload:

    @staticmethod
    def get_player_payload(event_type, player, **kwargs):
        payload = {
            'event_type': event_type,
            'id': player.id,
            'lv': player.lv,
            'next_lv': player.next_lv,
            'exp': player.exp,
            'max_hp': player.max_hp,
            'max_sp': player.max_sp,
            'current_hp': player.current_hp,
            'current_sp': player.current_sp,
            'hp': player.current_hp,
            'sp': player.current_sp,
            'power': player.power,
            'resistance': player.resistance,
            'agility': player.agility,
            'is_ko': player.is_ko,
            'x': player.position_x,
            'y': player.position_y,
            'position_x': player.position_x,
            'position_y': player.position_y,
            'area': player.area_location,
            'map_area': player.area_location,
            'classType': player.class_type,
            'name': player.name
        }
        payload.update(kwargs)
        return payload
