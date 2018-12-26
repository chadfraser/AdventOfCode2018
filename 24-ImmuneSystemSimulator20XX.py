class Group:
    def __init__(self, is_immune_system=True):
        self.is_immune_system = is_immune_system
        self.units_count = 0
        self.unit_hp = 0
        self.attack_type = None
        self.attack_damage = 0
        self.initiative = 0
        self.weaknesses = set()
        self.immunities = set()

    def add_weaknesses_and_immunities(self, passed_string):
        element_modifiers = passed_string.split(";")
        for current_string in element_modifiers:
            current_string = current_string.split()
            modifier = current_string[0]
            for element in current_string[2:]:
                if modifier == "weak":
                    self.weaknesses.add(element.strip(", "))
                elif modifier == "immune":
                    self.immunities.add(element.strip(", "))

    def get_effective_power(self):
        return self.units_count * self.attack_damage

    def get_attack_damage(self, target):
        if self.attack_type in target.immunities:
            return 0
        if self.attack_type in target.weaknesses:
            return self.get_effective_power() * 2
        return self.get_effective_power()

    def attack_target(self, target):
        damage = self.get_attack_damage(target)
        units_killed = damage // target.unit_hp
        target.units_count = max(0, target.units_count - units_killed)


def build_group_forces(file_data_list, is_immune_system=True, bonus_damage=0):
    all_groups = []
    for index, line in enumerate(file_data_list[1:], 1):
        if not line.strip():
            return all_groups, index
        split_line = line.split()
        new_group = Group(is_immune_system)
        new_group.units_count = int(split_line[0])
        new_group.unit_hp = int(split_line[4])
        if "(" in line and ")" in line:
            element_text = line[line.find("(")+1:line.find(")")]
            new_group.add_weaknesses_and_immunities(element_text)
        new_group.attack_damage = int(split_line[-6]) + bonus_damage
        new_group.attack_type = split_line[-5]
        new_group.initiative = int(split_line[-1])
        all_groups.append(new_group)
    return all_groups


def find_ideal_target(attacking_group, enemy_groups):
    enemy_groups.sort(key=lambda x: x.initiative, reverse=True)
    enemy_groups.sort(key=lambda x: x.get_effective_power(), reverse=True)
    enemy_groups.sort(key=lambda x: attacking_group.get_attack_damage(x), reverse=True)


def sort_groups_for_battle(total_groups):
    total_groups.sort(key=lambda group: group.initiative, reverse=True)
    total_groups.sort(key=lambda group: group.get_effective_power(), reverse=True)


def select_targets(immune_system_groups, infection_groups):
    total_groups = immune_system_groups + infection_groups
    sort_groups_for_battle(total_groups)
    attack_targets = {}
    for attacking_group in total_groups:
        if attacking_group.is_immune_system:
            untargeted_enemies = [group for group in infection_groups if group not in attack_targets.values()]
        else:
            untargeted_enemies = [group for group in immune_system_groups if group not in attack_targets.values()]
        find_ideal_target(attacking_group, untargeted_enemies)
        try:
            target = untargeted_enemies[0]
            if attacking_group.get_attack_damage(target) == 0:
                continue
            attack_targets[attacking_group] = target
        except IndexError:
            continue
    return total_groups, attack_targets


def attack_group(total_groups, attack_targets):
    total_groups.sort(key=lambda group: group.initiative, reverse=True)
    surviving_groups = {group for group in total_groups}
    for i, group in enumerate(total_groups, 1):
        if group.units_count == 0:
            continue
        try:
            # print(f"{group.is_immune_system} group {i} kills", end="")
            group.attack_target(attack_targets[group])
            if attack_targets[group].units_count == 0:
                surviving_groups.remove(attack_targets[group])
        except KeyError:
            continue
    immune_system_groups = [group for group in surviving_groups if group.is_immune_system]
    infection_groups = [group for group in surviving_groups if not group.is_immune_system]
    return immune_system_groups, infection_groups


def simulate_combat(immune_system_groups, infection_groups):
    while immune_system_groups and infection_groups:
        total_groups, attack_targets = select_targets(immune_system_groups, infection_groups)
        if not attack_targets:
            print("Combat ends in a stalemate.")
            return infection_groups, False
        immune_system_groups, infection_groups = attack_group(total_groups, attack_targets)
    if immune_system_groups:
        return immune_system_groups, True
    return infection_groups, False


def get_surviving_units_count(surviving_group):
    surviving_units_count = 0
    for group in surviving_group:
        surviving_units_count += group.units_count
    return surviving_units_count


def simulate_combat_until_victory(file_data):
    bonus_damage = 0
    immune_system_won = False
    surviving_groups = []
    while not immune_system_won:
        bonus_damage += 1
        immune_system_groups, starting_index = build_group_forces(file_data, is_immune_system=True,
                                                                  bonus_damage=bonus_damage)
        infection_groups = build_group_forces(file_data[starting_index + 1:], is_immune_system=False)
        surviving_groups, immune_system_won = simulate_combat(immune_system_groups, infection_groups)
    return surviving_groups


def main():
    with open("24-ImmuneSystemSimulator20XX-Input.txt") as input_file:
        file_data = input_file.readlines()

    immune_system_groups, starting_index = build_group_forces(file_data, is_immune_system=True)
    infection_groups = build_group_forces(file_data[starting_index+1:], is_immune_system=False)
    # for i, group in enumerate(immune_system_groups, 1):
    #     print(f"Group {i} contains {group.units_count} units. {group.attack_type} damage, {group.weaknesses} weaknesses, {group}")
    # print()
    # for i, group in enumerate(infection_groups, 1):
    #     print(f"Group {i} contains {group.units_count} units. {group.attack_type} damage, {group.weaknesses} weaknesses, {group}")
    # print()
    surviving_groups, immune_system_won = simulate_combat(immune_system_groups, infection_groups)
    surviving_units_count = get_surviving_units_count(surviving_groups)
    print(surviving_units_count)

    surviving_groups = simulate_combat_until_victory(file_data)
    surviving_units_count = get_surviving_units_count(surviving_groups)
    print(surviving_units_count)


if __name__ == "__main__":
    main()
