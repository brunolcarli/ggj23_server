import json
from math import ceil
from random import randint
from django.conf import settings
from server_app.map_areas import areas
from server_app.models import Character


def use_skill(skill_user, skill_name, target):
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
    # TODO broadcast skill using
    print(f'{skill_user.name} used {skill["name"]}')

    damage = get_damage(skill_user, skill['power'], target.resistance)
    target.current_hp -= damage
    # TODO broadcast damage
    print(f'{target.name} has lost {damage} HP due to {skill["name"]}')

    # Check if enemy is knockouted
    if target.current_hp <= 0:
        target.current_hp = 0
        target.is_ko = True
        # TODO broadcast knock out
        print(f'{target.name} was knockouted')

    if target.class_type == "enemy":
        if target.is_ko:
            # Enemy mobs give exp points
            skill_user.exp += target.exp
            # TODO broadcast exp gain
            print(f'{skill_user.name} has earned {target.exp} EXP')
            lv_up(skill_user)
    else:
        target.save()
    # TODO apply skill effect

    return True



def get_damage(skill_user, skill_power, target_resistance):
    damage = ((skill_user.power + skill_power - target_resistance) / 2) + (skill_user.lv * 2)

    if damage < 0:
        damage = 0

    return damage


def target_position_is_valid(target_position, map_area):
    x, y = target_position
    min_edge = x < 0 or y < 0
    max_edge = x > areas[map_area]['size_x'] or y > areas[map_area]['size_y']

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
        character.power += randint(0, 2)
        character.resistance += randint(0, 2)
        # TODO broadcast lv up
        print(f'{character.name} has leveled up to lv: {character.lv}')

    character.save()
    return character


def exp_up(character, value, factor=1):
    character.exp += value * factor

    if character.exp >= character.next_lv:
        character = lv_up(character)
        # TODO broadcast character lv up

    character.save()
