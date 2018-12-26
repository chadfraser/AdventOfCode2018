def find_manhattan_distance_between_points(point_a, point_b):
    distance = 0
    for coord_a, coord_b in zip(point_a, point_b):
        distance += abs(coord_a - coord_b)
    return distance


def find_constellation_count(disjoint_set_dict):
    disjoint_set = {frozenset(value) for value in disjoint_set_dict.values()}
    return len(disjoint_set)


def build_constellation_disjoint_sets(constellation_coordinates):
    disjoint_set_dict = {}
    for coordinate in constellation_coordinates:
        disjoint_set_dict[coordinate] = {coordinate}
        for coordinate_to_compare_to in disjoint_set_dict:
            if find_manhattan_distance_between_points(coordinate, coordinate_to_compare_to) <= 3:
                new_set = disjoint_set_dict[coordinate_to_compare_to].union(disjoint_set_dict[coordinate])
                for value in new_set:
                    disjoint_set_dict[value] = new_set
    return disjoint_set_dict


def parse_input_list(input_list):
    numeric_input_list = []
    for line in input_list:
        line = line.split(",")
        int_line = tuple(map(int, line))
        numeric_input_list.append(int_line)
    return numeric_input_list


def main():
    with open("25-FourDimensionalAdventure-Input.txt") as input_file:
        constellation_data = input_file.readlines()
    constellation_coordinates = parse_input_list(constellation_data)
    disjoint_set_dict = build_constellation_disjoint_sets(constellation_coordinates)
    disjoint_set_count = find_constellation_count(disjoint_set_dict)
    print(disjoint_set_count)


if __name__ == "__main__":
    main()
