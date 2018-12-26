from collections import Counter


def build_cave_2d_array(target_x, target_y):
    cave = [[0 for __ in range(target_x + 1)] for __ in range(target_y + 1)]
    return cave


def parse_cave_input(cave_input):
    depth = cave_input[0].split(": ")[1]
    depth = int(depth)
    target = cave_input[1].split(": ")[1]
    target_x, target_y = list(map(int, target.split(",")))
    return depth, target_x, target_y


def get_location_index_value(cave, depth, target_x, target_y, x, y):
    if x == y == 0 or (y == target_y and x == target_x):
        cave[y][x] = 0
    elif y == 0:
        cave[y][x] = x * 16807
    elif x == 0:
        cave[y][x] = y * 48271
    else:
        erosion_level_a = (cave[y][x - 1] + depth) % 20183
        erosion_level_b = (cave[y - 1][x] + depth) % 20183
        cave[y][x] = (erosion_level_a * erosion_level_b)


def get_location_index_for_all_locations(cave, depth, target_x, target_y):
    for y_index, sublist in enumerate(cave):
        for x_index, value in enumerate(sublist):
            get_location_index_value(cave, depth, target_x, target_y, x_index, y_index)


def get_erosion_index_value(cave, erosion_map, depth, x, y):
    erosion_value = (cave[y][x] + depth) % 20183
    if erosion_value % 3 == 0:
        erosion_map[y][x] = "."
    elif erosion_value % 3 == 1:
        erosion_map[y][x] = "="
    else:
        erosion_map[y][x] = "|"


def build_erosion_map(cave, depth):
    erosion_map = [["" for __ in range(len(cave[0]))] for __ in range(len(cave))]
    for y_index, sublist in enumerate(erosion_map):
        for x_index, value in enumerate(sublist):
            get_erosion_index_value(cave, erosion_map, depth, x_index, y_index)
    return erosion_map


def get_risk_level(erosion_map):
    erosion_counter = Counter([character for sublist in erosion_map for character in sublist])
    risk_level = erosion_counter["="] + erosion_counter["|"] * 2
    return risk_level


def get_risk_level_of_additional_area(erosion_map):
    erosion_counter = Counter([character for sublist in erosion_map for character in sublist])
    risk_level = erosion_counter["="] + erosion_counter["|"] * 2
    return risk_level


def aaaa(a):
    for y_index, sublist in enumerate(a):
        for x_index, value in enumerate(sublist):
            print(value, end="")
        print()


def main():
    with open("22-ModeMaze-Input.txt") as input_file:
        cave_data = input_file.readlines()
    depth, x, y = parse_cave_input(cave_data)
    print(depth, x, y)
    cave = build_cave_2d_array(x, y)
    get_location_index_for_all_locations(cave, depth, x, y)
    erosion_map = build_erosion_map(cave, depth)
    # aaaa(erosion_map)
    risk_level = get_risk_level(erosion_map)
    print(risk_level)


if __name__ == "__main__":
    main()
