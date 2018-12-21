from collections import Counter


def get_required_dimensions_of_reservoir(clay_locations):
    min_x_value = min(coord[0] for coord in clay_locations)
    max_x_value = max(coord[0] for coord in clay_locations)
    max_x_value = max(500, max_x_value)
    min_y_value = min(coord[1] for coord in clay_locations)
    max_y_value = max(coord[1] for coord in clay_locations)
    return min_x_value, max_x_value, min_y_value, max_y_value


def find_all_clay_locations(input_file_data):
    coordinate_locations_of_clay = []
    for line in input_file_data:
        start_element, length_elements = line.split(", ")
        starting_orientation, starting_value = start_element.split("=")
        starting_value = int(starting_value)

        length_orientation, length_values_list = length_elements.split("=")
        initial_length_value, end_length_value = length_values_list.split("..")
        initial_length_value = int(initial_length_value)
        end_length_value = int(end_length_value)

        if starting_orientation == "x":
            for value in range(initial_length_value, end_length_value + 1):
                coordinate_locations_of_clay.append((starting_value, value))
        else:
            for value in range(initial_length_value, end_length_value + 1):
                coordinate_locations_of_clay.append((value, starting_value))
    return coordinate_locations_of_clay


def build_reservoir_2d_array(clay_locations, min_x, max_x, max_y):
    reservoir_2d_array = [["." for __ in range(min_x - 1, max_x + 2)] for __ in range(max_y + 1)]
    for x, y in clay_locations:
        reservoir_2d_array[y][x - (min_x - 1)] = "#"
    reservoir_2d_array[0][500 - (min_x - 1)] = "+"
    return reservoir_2d_array


def is_clay(reservoir, x, y):
    try:
        value = reservoir[y][x]
    except IndexError:
        return False
    return value == "#"


def is_water(reservoir, x, y):
    try:
        value = reservoir[y][x]
    except IndexError:
        return False
    return value in ["~", "|"]


def make_water_fall(reservoir, x, y):
    while True:
        y += 1
        try:
            current_value = reservoir[y][x]
            if current_value == ".":
                reservoir[y][x] = "|"
            else:
                break
        except IndexError:
            break
    return x, y


def move_water(reservoir, x, y, moving_left=True):
    bordered_on_side = False
    while True:
        try:
            current_value = reservoir[y][x]
            lower_value = reservoir[y + 1][x]
            if current_value == "#":
                bordered_on_side = True
                break
            reservoir[y][x] = "|"
            if lower_value in [".", "|"]:
                break
        except IndexError:
            break

        if moving_left:
            x -= 1
        else:
            x += 1
    return bordered_on_side, (x, y)


def move_water_on_both_sides(reservoir, x, y):
    bordered_on_left, left_edge_coordinates = move_water(reservoir, x, y)
    bordered_on_right, right_edge_coordinates = move_water(reservoir, x, y, moving_left=False)

    bordered_on_both_sides = bordered_on_left and bordered_on_right
    return bordered_on_both_sides, [left_edge_coordinates, right_edge_coordinates]


def make_water_rest(reservoir, x, y, moving_left=True):
    current_value = reservoir[y][x]
    while current_value != "#":
        reservoir[y][x] = "~"
        if moving_left:
            x -= 1
        else:
            x += 1
        current_value = reservoir[y][x]


def make_water_rest_on_both_sides(reservoir, x, y):
    make_water_rest(reservoir, x, y)
    make_water_rest(reservoir, x, y, moving_left=False)


def make_water_spread(reservoir, x, y, edge_water_coordinates=None):
    if edge_water_coordinates is None:
        edge_water_coordinates = []

    bordered_on_both_sides, edge_coordinates = move_water_on_both_sides(reservoir, x, y)
    for (edge_x, edge_y) in edge_coordinates:
        if not is_clay(reservoir, edge_x, edge_y) and not(edge_x, edge_y) == (x, y):
            edge_water_coordinates.append((edge_x, edge_y))
    if bordered_on_both_sides:
        make_water_rest_on_both_sides(reservoir, x, y)
        make_water_spread(reservoir, x, y - 1, edge_water_coordinates)
    return edge_water_coordinates


def flow_water(reservoir):
    spring_coordinates = (reservoir[0].index("+"), 0)
    coordinates_to_fall_from = [spring_coordinates]
    while coordinates_to_fall_from:
        edge_coordinates = []
        (x, y) = coordinates_to_fall_from.pop()
        new_x, new_y = make_water_fall(reservoir, x, y)
        if (new_x, new_y) != (x, y) and (is_clay(reservoir, new_x, new_y) or is_water(reservoir, new_x, new_y)):
            edge_coordinates = make_water_spread(reservoir, new_x, new_y - 1)
        coordinates_to_fall_from.extend(edge_coordinates)


def count_water_tiles(reservoir):
    water_counter = Counter([character for sublist in reservoir for character in sublist])
    return water_counter["~"] + water_counter["|"]


def count_resting_water_tiles(reservoir):
    water_counter = Counter([character for sublist in reservoir for character in sublist])
    return water_counter["~"]


def main():
    with open("17-ReservoirResearch-Input.txt") as input_file:
        reservoir_coords_data = input_file.readlines()
    clay_locations = find_all_clay_locations(reservoir_coords_data)
    min_x, max_x, min_y, max_y = get_required_dimensions_of_reservoir(clay_locations)
    reservoir = build_reservoir_2d_array(clay_locations, min_x, max_x, max_y)
    flow_water(reservoir)

    water_count = count_water_tiles(reservoir[min_y:])
    resting_water_count = count_resting_water_tiles(reservoir[min_y:])

    print(water_count)
    print(resting_water_count)


if __name__ == "__main__":
    main()
