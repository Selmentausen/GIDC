my_data = {'char_atk': 1308, 'elem_bonus': 7, 'special_bonus': 87,
        'talent_multi': '326', 'char_lvl': 70, 'crit_rate': 10.8,
        'crit_dmg': 120.7, 'attack_count': 10, 'enemy_lvl': 86,
        'enemy_elem_res': 10, 'enemy_phys_res': 50, 'dmg_type': 'elemental'}


def calculate_resistance_damage_reduction(resistance) -> float:
    return 1 - resistance / 100


def calculate_defense_damage_reduction(enemy_level, character_level) -> float:
    defense = 5 * enemy_level + 500
    return 1 - defense / (defense + 5 * character_level + 500)


def get_enemy_reduction(data) -> tuple:
    base_resistance = data['enemy_elem_res'] if data['dmg_type'] == 'elemental' else data['enemy_phys_res']
    resistance_damage_reduction = calculate_resistance_damage_reduction(base_resistance)
    defense_damage_reduction = calculate_defense_damage_reduction(data['enemy_lvl'], data['char_lvl'])
    return resistance_damage_reduction, defense_damage_reduction


def calculate_attack_bonus_multiplier(special_bonus, elem_bonus):
    return 1 + ((special_bonus + elem_bonus) / 100)


def parse_talent_multipliers(talent_multiplier_text) -> list:
    # talent_multiplier_text should be string containing numbers separated by semicolon(;)
    multipliers = list(map(lambda x: float(x.strip()), talent_multiplier_text.split(';')))
    return multipliers


def calculate_average_talent_multiplier(talent_multipliers) -> float:
    return (sum(talent_multipliers) / len(talent_multipliers)) / 100


def get_character_damage(data) -> int:
    bonus_multiplier = calculate_attack_bonus_multiplier(data['special_bonus'], data['elem_bonus'])
    talent_multiplier = calculate_average_talent_multiplier(parse_talent_multipliers(data['talent_multi']))
    return round(data['char_atk'] * bonus_multiplier * talent_multiplier)


def calculate_crictical_hit_damage(single_hit_damage, critical_multiplier) -> int:
    return round(single_hit_damage * (1 + critical_multiplier / 100))


def calculate_critical_hit_amount(attack_count, critical_hit_rate) -> int:
    return round(attack_count * (critical_hit_rate / 100))


def get_total_attack_hit_damage(single_hit_damage, single_critical_hit_damage, data) -> int:
    critical_hit_amount = calculate_critical_hit_amount(data['attack_count'], data['crit_rate'])
    total_critical_hit_damage = single_critical_hit_damage * critical_hit_amount
    total_damage = total_critical_hit_damage + (single_hit_damage * (data['attack_count'] - critical_hit_amount))
    return round(total_damage)


def get_damage_calculations(data) -> (int, int, int):
    # returns (single attack damage, single critical attack damage, total attack damage)
    enemy_resistance_reduction, enemy_defense_reduction = get_enemy_reduction(data)
    character_damage = get_character_damage(data)
    single_hit_damage = round(character_damage * enemy_defense_reduction * enemy_resistance_reduction)
    single_critical_hit_damage = calculate_crictical_hit_damage(single_hit_damage, data['crit_dmg'])
    total_hit_damage = get_total_attack_hit_damage(single_hit_damage, single_critical_hit_damage, data)
    return single_hit_damage, single_critical_hit_damage, total_hit_damage
