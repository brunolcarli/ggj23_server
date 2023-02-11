import requests
from base64 import b64encode
import json
from math import ceil
from random import randint
from django.conf import settings
from server_app.map_areas import areas
from server_app.models import Character
from server_app.events import OnCharacterEvent


def use_skill(skill_user, skill_name, target, class_type):
    """
    Targeted enemy based skill usage mechanic. 
    """
    if skill_user.is_ko:
        raise Exception('Cannot perform this action while knocked out')

    skillset = json.loads(skill_user.skills.decode('utf-8'))
    if skill_name not in skillset:
        raise Exception('Invalid or unlearned skill')

    skill = skillset[skill_name]

    if not reachable_target(skill_user, target, skill['range']):
        raise Exception('Unreachable position')

    if skill['sp_cost'] > skill_user.current_sp:
        raise Exception('Not enough SP')

    skill_user.current_sp -= skill['sp_cost']
    skill_user.save()
    
    # broadcast skill using
    payload = {
        'skill_user_id': skill_user.id,
        'skill_user_name': skill_user.name,
        'skill_name': skill["name"],
        'target_id': target.id,
        'target_name': target.name,
        'target_class_type': class_type,
        'area': skill_user.area_location
    }
    OnCharacterEvent.char_event(params={
        'event_type': 'character_use_skill',
        'data': payload
    })

    damage = get_damage(skill_user, skill['power'], target.resistance)
    target.current_hp -= damage
    target.save()
    
    # broadcast damage
    payload = {
        'target_id': target.id,
        'target_name': target.name,
        'target_hp': target.current_hp,
        'damage': damage,
        'skill_name': skill['name'],
        'skill_user_id': skill_user.id,
        'skill_user_sp': skill_user.current_sp,
        'area': skill_user.area_location,
        'classType': class_type
    }
    OnCharacterEvent.char_event(params={
        'event_type': 'target_damaged',
        'data': payload
    })

    # Check if enemy is knockouted
    if target.current_hp <= 0:
        target.current_hp = 0
        target.is_ko = True
        # broadcast knock out
        payload = {
            'target_id': target.id,
            'target_name': target.name,
            'target_is_ko': target.is_ko,
            'target_hp': target.current_hp,
            'area': target.area_location,
            'classType': class_type
        }
        OnCharacterEvent.char_event(params={
            'event_type': 'target_knockout',
            'data': payload
        })

    if target.class_type == "enemy":
        if target.is_ko:
            # Enemy mobs give exp points
            skill_user.exp += target.exp
            lv_up(skill_user)
            
            # broadcast exp gain
            payload = {
                'skill_user_id': skill_user.id,
                'exp': target.exp,
                'lv': skill_user.lv,
                'area': skill_user.area_location,
                'classType': class_type
            }
            OnCharacterEvent.char_event(params={
                'event_type': 'character_exp_gain',
                'data': payload
            })
            target.delete()
            
    else:
        target.save()
    skill_user.save()
    # TODO apply skill effect

    return True


def get_damage(skill_user, skill_power, target_resistance):
    damage = ((skill_user.power + skill_power - target_resistance) / 2) + (skill_user.lv * 2)

    if damage < 0:
        damage = 0

    return int(damage)


def target_position_is_valid(target_position, map_area):
    x, y = target_position
    min_edge = x < 14 or y < 14
    max_edge = x > areas[map_area]['size_x']-14 or y > areas[map_area]['size_y']-14

    return not (min_edge or max_edge)


def reachable_target(skill_user, target, skill_range):
    cx, cy = skill_user.position_x, skill_user.position_y
    tx, ty = target.position_x, target.position_y
    skill_range = skill_range * 48

    x_diff = abs(cx - tx)
    y_diff = abs(cy - ty)
    
    return x_diff <= skill_range and y_diff <= skill_range


def next_lv(level):
    """
    Calculates the amount Exp needed to level up based on the current level.
    param : level : <int>
    """
    return ceil((2 * (level ** 2.6)) / 2)


def lv_up(character):
    """
    Levels up a character, if possible.
    """
    config = settings.GAME_CONFIG
    while character.exp >= character.next_lv and character.lv < config['MAX_LV']:
        character.lv += 1
        character.next_lv = next_lv(character.lv)

        character.max_hp += randint(10, 50)
        character.max_sp += randint(5, 25)
        character.current_hp = character.max_hp
        character.current_sp = character.max_sp
        character.power += randint(0, 2)
        character.resistance += randint(0, 2)
        character.ep += 2

        # broadcast lv up
        payload = {
            'id': character.id,
            'lv': character.lv,
            'area': character.area_location,
            'max_hp': character.max_hp,
            'current_hp': character.max_hp,
            'max_sp': character.max_sp,
            'current_sp': character.max_sp,
            'classType': character.class_type
        }
        query = f'''
                mutation{{
                    notifyEnemyEvent(input:{{
                        eventType: "character_lv_up"
                        data: "{b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8')}"
                    }}){{
                    result
                    }}
                }}
            '''
        requests.post(
            settings.GQL_URL,
            json={'query': query}
        )

    character.save()
    return character


def exp_up(character, value, factor=1):
    character.exp += value * factor

    if character.exp >= character.next_lv:
        character = lv_up(character)

    character.save()
