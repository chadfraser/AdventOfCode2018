def parse_data(plant_data):
    initial_state = plant_data[0].split()[-1]
    dict_of_rules = {}
    for line in plant_data[2:]:
        pot_layout, __, result = line.split()
        dict_of_rules[pot_layout] = result
    return initial_state, dict_of_rules


def spread_plants(current_state, dict_of_rules, initial_index):
    minimum_number_to_append_left = 5
    for num in range(1, 6):
        if set(current_state[:num]) == {"."}:
            minimum_number_to_append_left -= 1
        else:
            break

    minimum_number_to_append_right = 5
    for num in range(1, 6):
        if set(current_state[-num:]) == {"."}:
            minimum_number_to_append_right -= 1
        else:
            break

    initial_index -= minimum_number_to_append_left
    left_append_state = "." * minimum_number_to_append_left
    right_append_state = "." * minimum_number_to_append_right
    current_state = left_append_state + current_state + right_append_state

    new_state = current_state[0:4]
    for num, plant in enumerate(current_state[4:-4], 4):
        plant_state = current_state[num-2 : num+3]
        plant_result = dict_of_rules[plant_state]
        new_state += plant_result
    new_state += current_state[-4:]
    return new_state, initial_index


def get_index_and_state_over_time(initial_state, dict_of_rules, length_of_time=20):
    current_state = initial_state
    current_index = 0

    for __ in range(length_of_time):
        current_state, current_index = spread_plants(current_state, dict_of_rules, current_index)
    return current_state, current_index


def get_index_and_state_until_repetition(initial_state, dict_of_rules, maximum_iterations=10000):
    current_state = initial_state
    current_index = 0
    list_of_all_states = []
    current_time = 0

    for __ in range(maximum_iterations):
        current_time += 1
        current_state, current_index = spread_plants(current_state, dict_of_rules, current_index)
        list_of_all_states, repetition_time = find_repetition(current_state, list_of_all_states)
        if repetition_time is not None:
            repetition_state, repetition_index = get_index_and_state_over_time(initial_state, dict_of_rules,
                                                                               length_of_time=repetition_time)
            return (repetition_state, repetition_index, repetition_time), (current_state, current_index, current_time)

    else:
        raise Exception(f"Did not find a repetition within {maximum_iterations} iterations.")


def find_repetition(current_state, list_of_all_states):
    current_plant_layout = current_state.strip(".")
    if current_plant_layout in list_of_all_states:
        return list_of_all_states, list_of_all_states.index(current_plant_layout) + 1
    else:
        list_of_all_states.append(current_plant_layout)
        return list_of_all_states, None


def sum_plant_values(final_state, index):
    final_sum = 0
    for num, value in enumerate(final_state, index):
        if value == "#":
            final_sum += num
    return final_sum


def extrapolate_and_sum_plant_values(base_data, repetition_data, final_time, dict_of_rules):
    base_state, base_index, base_time = base_data
    repetition_state, repetition_index, repetition_time = repetition_data

    period_length = repetition_time - base_time
    difference_of_indexes = repetition_index - base_index

    base_left_dot_amount = len(base_state) - len(base_state.lstrip("."))
    repetition_left_dot_amount = len(repetition_state) - len(repetition_state.lstrip("."))
    difference_of_dot_amounts = repetition_left_dot_amount - base_left_dot_amount

    remaining_time = final_time - repetition_time
    required_time_at_end_of_last_period = remaining_time % period_length
    index_at_end_of_last_period = remaining_time * difference_of_indexes

    final_state = base_state
    final_index = repetition_index + (difference_of_dot_amounts * remaining_time) + 1

    for __ in range(required_time_at_end_of_last_period):
        final_state, final_index = get_index_and_state_over_time(base_state, dict_of_rules,
                                                                 length_of_time=required_time_at_end_of_last_period)
        final_index += index_at_end_of_last_period

    final_sum = sum_plant_values(final_state, final_index)
    return final_sum


def main():
    with open("12-SubterraneanSustainability-Input.txt") as input_file:
        plant_data = input_file.readlines()
    initial_state, dict_of_rules = parse_data(plant_data)

    final_state, final_initial_index = get_index_and_state_over_time(initial_state, dict_of_rules)
    print(final_state, final_initial_index)

    final_sum = sum_plant_values(final_state, final_initial_index)
    print(final_sum)

    base_data, repetition_data = get_index_and_state_until_repetition(initial_state, dict_of_rules)
    final_sum = extrapolate_and_sum_plant_values(base_data, repetition_data, 50_000_000_000, dict_of_rules)
    print(final_sum)


if __name__ == "__main__":
    main()
