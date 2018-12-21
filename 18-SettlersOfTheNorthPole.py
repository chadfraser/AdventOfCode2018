from collections import Counter


def get_lumber_value(landscape):
    lumber_counter = Counter([character for sublist in landscape for character in sublist])
    return lumber_counter["|"] * lumber_counter["#"]


def get_sum_of_adjacent_tiles(landscape, x, y):
    open_acre_count = tree_count = lumberyard_count = 0
    for y_value in range(-1, 2):
        for x_value in range(-1, 2):
            if not 0 <= y + y_value < len(landscape) or not 0 <= x + x_value < len(landscape[y_value]):
                continue
            if x_value == y_value == 0:
                continue
            try:
                value = landscape[y + y_value][x + x_value]
                if value == ".":
                    open_acre_count += 1
                elif value == "|":
                    tree_count += 1
                elif value == "#":
                    lumberyard_count += 1
            except IndexError:
                pass
    return open_acre_count, tree_count, lumberyard_count


def alter_open_acre(tree_count):
    if tree_count >= 3:
        return "|"
    return "."


def alter_tree(lumberyard_count):
    if lumberyard_count >= 3:
        return "#"
    return "|"


def alter_lumberyard(tree_count, lumberyard_count):
    if lumberyard_count >= 1 and tree_count >= 1:
        return "#"
    return "."


def alter_landscape(landscape):
    new_landscape = []
    for y_index, sublist in enumerate(landscape):
        temp_sublist = []
        for x_index, value in enumerate(sublist):
            open_acre_count, tree_count, lumberyard_count = get_sum_of_adjacent_tiles(landscape, x_index, y_index)
            if value == ".":
                temp_sublist.append(alter_open_acre(tree_count))
            elif value == "|":
                temp_sublist.append(alter_tree(lumberyard_count))
            else:
                temp_sublist.append(alter_lumberyard(tree_count, lumberyard_count))
        new_landscape.append(temp_sublist)
    return new_landscape


def build_landscape(landscape_file_data):
    landscape = []
    for line in landscape_file_data:
        temp_list = list(line.strip())
        landscape.append(temp_list)
    return landscape


def alter_lumberyard_until_repetition(initial_landscape, maximum_iterations=10000):
    current_landscape = initial_landscape
    list_of_all_landscapes = []
    current_time = 0

    for __ in range(maximum_iterations):
        current_time += 1
        current_landscape = alter_landscape(current_landscape)
        list_of_all_states, base_time = find_repetition(current_landscape, list_of_all_landscapes)
        if base_time is not None:
            return current_time, base_time, current_landscape
    else:
        raise Exception(f"Did not find a repetition within {maximum_iterations} iterations.")


def find_repetition(current_yard, list_of_all_yards):
    current_yard_flat_list = [value for sublist in current_yard for value in sublist]
    if current_yard_flat_list in list_of_all_yards:
        return list_of_all_yards, list_of_all_yards.index(current_yard_flat_list) + 1
    else:
        list_of_all_yards.append(current_yard_flat_list)
        return list_of_all_yards, None


def extrapolate_and_get_lumber_value(landscape, base_time, repetition_time, final_time):
    period_length = repetition_time - base_time
    remaining_time = final_time - repetition_time
    required_time_at_end_of_last_period = remaining_time % period_length
    for __ in range(required_time_at_end_of_last_period):
        landscape = alter_landscape(landscape)

    lumber_value = get_lumber_value(landscape)
    return lumber_value


def main():
    with open("18-SettlersOfTheNorthPole-Input.txt") as input_file:
        landscape_file_data = input_file.readlines()
    landscape = build_landscape(landscape_file_data)
    for __ in range(10):
        landscape = alter_landscape(landscape)

    lumber_value = get_lumber_value(landscape)
    print(lumber_value)

    base_landscape = build_landscape(landscape_file_data)
    repetition_time, base_time, base_landscape = alter_lumberyard_until_repetition(base_landscape)
    final_value = extrapolate_and_get_lumber_value(base_landscape, base_time, repetition_time, 1_000_000_000)
    print(final_value)


if __name__ == "__main__":
    main()
