from collections import deque


class Entity:
    def __init__(self, x, y, character, attack=3):
        self.x = x
        self.y = y
        self.character = character
        self.health = 200
        self.attack = attack
        self.last_round_acted = -1

    def __str__(self):
        return self.character

    def __repr__(self):
        return "'" + self.character + "'"


def get_target_character(current_player):
    if current_player.character == "E":
        return "G"
    return "E"


def determine_if_space_contains_target(value, target):
    return isinstance(value, Entity) and value.character == target


def determine_if_enemy_combatants_exist(coordinates_2d_array, x, y):
    current_turn_player = coordinates_2d_array[y][x]
    target = get_target_character(current_turn_player)
    for sub_array in coordinates_2d_array:
        for value in sub_array:
            if determine_if_space_contains_target(value, target):
                return True
    return False


def is_character_adjacent_to_target(coordinates_2d_array, x, y):
    current_turn_player = coordinates_2d_array[y][x]
    target = get_target_character(current_turn_player)

    if any(determine_if_space_contains_target(value, target) for value in [coordinates_2d_array[y - 1][x],
                                                                           coordinates_2d_array[y][x - 1],
                                                                           coordinates_2d_array[y][x + 1],
                                                                           coordinates_2d_array[y + 1][x]]):
        return True
    return False


def find_all_empty_squares_adjacent_to_all_targets(coordinates_2d_array, x, y):
    current_character = coordinates_2d_array[y][x]
    target = get_target_character(current_character)

    offsets = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    set_of_empty_tiles_adjacent_to_targets = set()

    for y_val, sub_array in enumerate(coordinates_2d_array):
        for x_val, character in enumerate(sub_array):
            if determine_if_space_contains_target(character, target):
                for x_offset, y_offset in offsets:
                    adjacent_character = coordinates_2d_array[y_val + y_offset][x_val + x_offset]
                    if adjacent_character == ".":
                        set_of_empty_tiles_adjacent_to_targets.add((x_val + x_offset, y_val + y_offset))
    return set_of_empty_tiles_adjacent_to_targets


def find_nearest_target(coordinates_2d_array, x, y):
    set_of_target_tiles = find_all_empty_squares_adjacent_to_all_targets(coordinates_2d_array, x, y)

    offsets = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    coordinates_checked = {(x, y): (None, None, 0)}
    search_deque = deque([(x, y, 0)])

    while search_deque:
        x, y, distance = search_deque.popleft()

        for offset_x, offset_y in offsets:
            if coordinates_2d_array[y + offset_y][x + offset_x] == "." and \
                    (x + offset_x, y + offset_y) not in coordinates_checked:
                search_deque.append((x + offset_x, y + offset_y, distance + 1))
                coordinates_checked[(x + offset_x, y + offset_y)] = (x, y, distance + 1)

    reachable_target_tiles = [(coord, previous) for coord, previous in coordinates_checked.items()
                              if coord in set_of_target_tiles]
    if reachable_target_tiles:
        minimum_distance = min(reachable_target_tiles, key=lambda coord: coord[1][-1])[1][-1]
        reachable_target_tiles = [(coord, previous) for coord, previous in reachable_target_tiles
                                  if previous[-1] == minimum_distance]
        if reachable_target_tiles:
            reachable_target_tiles.sort(key=lambda coord: coord[0][0])
            reachable_target_tiles.sort(key=lambda coord: coord[0][1])
            target_tile, previous_tile = reachable_target_tiles[0]
            return (target_tile, previous_tile[:-1]), coordinates_checked
    return None, None


def find_nearest_move(coordinates_2d_array, x, y):
    nearest_target_adjacent_coordinates, dict_of_coordinates_checked = find_nearest_target(coordinates_2d_array, x, y)
    if nearest_target_adjacent_coordinates is None:
        return
    (current_move, previous_move) = nearest_target_adjacent_coordinates
    while previous_move != (x, y):
        current_move, previous_move = previous_move, dict_of_coordinates_checked[previous_move][:-1]
    return current_move


def move_character(coordinates_2d_array, x, y):
    if is_character_adjacent_to_target(coordinates_2d_array, x, y):
        return x, y

    current_move = find_nearest_move(coordinates_2d_array, x, y)
    if current_move is not None:
        new_x, new_y = current_move
        coordinates_2d_array[new_y][new_x] = coordinates_2d_array[y][x]
        coordinates_2d_array[y][x] = "."
        x, y = new_x, new_y
    return x, y


def choose_attack_target(coordinates_2d_array, x, y):
    target = get_target_character(coordinates_2d_array[y][x])

    adjacent_health_values = []
    for temp_x, temp_y in [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]:
        value = coordinates_2d_array[temp_y][temp_x]
        if determine_if_space_contains_target(value, target):
            adjacent_health_values.append((value, value.health, temp_x, temp_y))
        else:
            adjacent_health_values.append((None, float("inf"), 0, 0))

    final_target = final_target_x = final_target_y = None
    minimum_health = float("inf")
    for current_target, current_health, current_x, current_y in adjacent_health_values:
        if current_health < minimum_health:
            minimum_health = current_health
            final_target = current_target
            final_target_x, final_target_y = current_x, current_y
    return final_target, final_target_x, final_target_y


def attack_with_character(coordinates_2d_array, x, y):
    if not is_character_adjacent_to_target(coordinates_2d_array, x, y):
        return

    final_target, final_target_x, final_target_y = choose_attack_target(coordinates_2d_array, x, y)
    if final_target:
        final_target.health = max(final_target.health - coordinates_2d_array[y][x].attack, 0)
        if final_target.health == 0:
            coordinates_2d_array[final_target_y][final_target_x] = "."
            if final_target.character == "E":
                return True


def get_total_health_of_all_remaining_combatants(coordinates_2d_array):
    characters_to_move = []
    for y_val, sub_array in enumerate(coordinates_2d_array):
        for x_val, character in enumerate(sub_array):
            if isinstance(character, Entity):
                characters_to_move.append((x_val, y_val))

    total_winning_side_health = 0
    for (x, y) in characters_to_move:
        total_winning_side_health += coordinates_2d_array[y][x].health
    return total_winning_side_health


def build_2d_array_of_map(map_data, attack_value=3):
    map_2d_array = []
    for y_val, data_string in enumerate(map_data):
        temp_list = []
        for x_val, element in enumerate(data_string.strip()):
            if element == "E":
                temp_list.append(Entity(x_val, y_val, element, attack_value))
            elif element == "G":
                temp_list.append(Entity(x_val, y_val, element))
            else:
                temp_list.append(element)
        map_2d_array.append(temp_list)
    return map_2d_array


def run_battle_simulator(coordinates_2d_array):
    current_round = 0
    while True:
        characters_to_move = []
        for y_val, sub_array in enumerate(coordinates_2d_array):
            for x_val, character in enumerate(sub_array):
                if isinstance(character, Entity):
                    characters_to_move.append((x_val, y_val))

        for (x, y) in characters_to_move:
            if isinstance(coordinates_2d_array[y][x], Entity) and \
                    coordinates_2d_array[y][x].last_round_acted < current_round and \
                    coordinates_2d_array[y][x].health > 0:
                if not determine_if_enemy_combatants_exist(coordinates_2d_array, x, y):
                    return coordinates_2d_array, current_round
                coordinates_2d_array[y][x].last_round_acted = current_round
                new_x, new_y = move_character(coordinates_2d_array, x, y)
                attack_with_character(coordinates_2d_array, new_x, new_y)
        current_round += 1


def run_battle_simulator_until_victory(coordinates_2d_array):
    current_round = 0
    while True:
        characters_to_move = []
        for y_val, sub_array in enumerate(coordinates_2d_array):
            for x_val, character in enumerate(sub_array):
                if isinstance(character, Entity):
                    characters_to_move.append((x_val, y_val))

        for (x, y) in characters_to_move:
            if isinstance(coordinates_2d_array[y][x], Entity) and \
                    coordinates_2d_array[y][x].last_round_acted < current_round and \
                    coordinates_2d_array[y][x].health > 0:
                if not determine_if_enemy_combatants_exist(coordinates_2d_array, x, y):
                    if coordinates_2d_array[y][x].character == "E":
                        return coordinates_2d_array, current_round, True
                    return coordinates_2d_array, current_round, False
                coordinates_2d_array[y][x].last_round_acted = current_round
                new_x, new_y = move_character(coordinates_2d_array, x, y)
                elf_lost = attack_with_character(coordinates_2d_array, new_x, new_y)
                if elf_lost:
                    return coordinates_2d_array, current_round, False
        current_round += 1


def main():
    with open("15-BeverageBandits-Input.txt") as input_file:
        map_file_data = input_file.readlines()
    map_2d_array = build_2d_array_of_map(map_file_data)
    map_2d_array, current_round = run_battle_simulator(map_2d_array)

    total_winning_side_health = get_total_health_of_all_remaining_combatants(map_2d_array)
    print(current_round, total_winning_side_health, current_round * total_winning_side_health)

    is_victory = False
    current_attack_power = 3
    while not is_victory:
        current_attack_power += 1
        with open("15-BeverageBandits-Input.txt") as input_file:
            map_file_data = input_file.readlines()
        map_2d_array = build_2d_array_of_map(map_file_data, current_attack_power)
        map_2d_array, current_round, is_victory = run_battle_simulator_until_victory(map_2d_array)
    print(current_attack_power)

    total_winning_side_health = get_total_health_of_all_remaining_combatants(map_2d_array)
    print(current_round, total_winning_side_health, current_round * total_winning_side_health)


if __name__ == "__main__":
    main()
