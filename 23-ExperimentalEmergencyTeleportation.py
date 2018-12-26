def find_manhattan_distance_between_points(point_a, point_b):
    distance = 0
    for coord_a, coord_b in zip(point_a, point_b):
        distance += abs(coord_a - coord_b)
    return distance


def get_nanobot_data(data_list):
    nanobot_data = []
    for line in data_list:
        position_data, radius_data = line.strip().split()
        radius = int(radius_data[2:])
        position_data = position_data.split(",")
        x = int(position_data[0][5:])
        y = int(position_data[1])
        z = int(position_data[2][:-1])
        nanobot_data.append([x, y, z, radius])
    return nanobot_data


def sort_nanobot_strength(nanobot_data):
    nanobot_data.sort(key=lambda x: x[-1], reverse=True)


def find_nanobots_in_range(target_nanobot, nanobot_list):
    radius_range = target_nanobot[-1]
    nanobots_in_range = 0
    for nanobot in nanobot_list:
        if find_manhattan_distance_between_points(nanobot[:-1], target_nanobot[:-1]) <= radius_range:
            nanobots_in_range += 1
        else:
            print(find_manhattan_distance_between_points(nanobot[:-1], target_nanobot[:-1]))
    return nanobots_in_range


def find_optimal_coordinate(nanobot_data):
    pass


def main():
    with open("23-ExperimentalEmergencyTeleportation-Input.txt") as input_file:
        nanobot_data_list = input_file.readlines()
    nanobot_data = get_nanobot_data(nanobot_data_list)
    sort_nanobot_strength(nanobot_data)
    print(nanobot_data)
    nanobots_in_range = find_nanobots_in_range(nanobot_data[0], nanobot_data)
    print(nanobot_data[0])
    print(nanobot_data[0][-1])
    print(nanobots_in_range)


if __name__ == "__main__":
    main()
