import json
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

    # TODO apply skill effect

    target.save()

    return True



def get_damage(skill_user, skill_power, target_resistance):
    damage = ((skill_user.power + skill_power - target_resistance) / 2) + (skill_user.lv * 2)

    if damage < 0:
        damage = 0

    return damage


def target_position_is_valid(target_position, map_area):
    x, y = target_position
    min_edge = x < 0 or y < 0
    max_edge = x > map_area['size_x'] or y > map_area['size_y']

    return not (min_edge or max_edge)


def reachable_target(skill_user, target, skill_range):
    cx, cy = skill_user.position_x, skill_user.position_y
    tx, ty = target.position_x, target.position_y
    skill_range = skill_range * 48

    if cx < tx:
        x_reach = abs(tx - cx) <= skill_range
    else:
        x_reach = abs(cx - tx) <= skill_range

    if cy < ty:
        y_reach = abs(ty - cy) <= skill_range
    else:
        y_reach = abs(cy - ty) <= skill_range

    return x_reach or y_reach
