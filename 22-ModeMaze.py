from collections import Counter
from queue import PriorityQueue


def build_cave_2d_array(target_x, target_y):
    cave = [[0 for __ in range(target_x + 100)] for __ in range(target_y + 100)]
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


def switch_equipment(current_region, current_equip):
    swappable_items = {".": ["torch", "climbing gear"], "=": ["neither", "climbing gear"],
                       "|": ["neither", "torch"]}
    items_swapping = swappable_items[current_region]
    item_to_swap = [item for item in items_swapping if item != current_equip][0]
    return item_to_swap
    # if current_region == ".":
    #     if current_equip == "torch":
    #         return "climbing gear"
    #     else:
    #         return "torch"
    # elif current_region == "=":
    #     if current_equip == "climbing gear":
    #         return "neither"
    #     else:
    #         return "climbing gear"
    # else:
    #     if current_equip == "torch":
    #         return "neither"
    #     else:
    #         return "torch"


def cannot_enter_region(current_region, current_equip):
    unusable_items = {".": "neither", "=": "torch", "|": "climbing gear"}
    return unusable_items[current_region] == current_equip
    # all_usable_items_test = [unusable_items[current_region] == equip for equip in current_equip_set]
    # return all(all_usable_items_test)
    # if current_region == ".":
    #     return current_equip == "neither"
    # elif current_region == "=":
    #     return current_equip == "torch"
    # else:
    #     return current_equip == "climbing gear"


# def aaa(x, y, time_and_equip_dict, time_to_coord, new_equip, search_queue):
#     previous_equip_set = set()
#     try:
#         if time_and_equip_dict[(x, y)][0] == time_to_coord:
#             previous_equip_set = time_and_equip_dict[(x, y)][1]
#             # if previous_equip_set != new_equip_set:
#             #     print("AA", previous_equip_set, new_equip_set)
#     except KeyError:
#         pass
#     new_equip_set |= previous_equip_set
#     search_queue.put((time_to_coord, ((x, y), new_equip_set)))
#     time_and_equip_dict[(x, y)] = (time_to_coord, new_equip_set)


def modified_search(erosion_map, target_x, target_y):
    current_equip = "torch"
    offsets = [(0, -1), (-1, 0), (1, 0), (0, 1)]

    equip_time_coord_dicts = {"torch": {(0, 0): 0}, "climbing gear": {}, "neither": {}}
    search_queue = PriorityQueue()
    search_queue.put((0, ((0, 0), current_equip)))

    while search_queue:
        current_time, ((x, y), current_equip) = search_queue.get()
        for x_offset, y_offset in offsets:
            new_x, new_y = x + x_offset, y + y_offset
            if 0 <= new_x < len(erosion_map[0]) and 0 <= new_y < len(erosion_map):
                time_to_coord = current_time + 1
                new_equip = current_equip
                current_region = erosion_map[new_y][new_x]

                if cannot_enter_region(current_region, current_equip):
                    time_to_coord += 7
                    new_equip = switch_equipment(erosion_map[y][x], current_equip)
                current_coord_dict = equip_time_coord_dicts[new_equip]

                if (new_x, new_y) not in current_coord_dict or current_coord_dict[(new_x, new_y)] >= time_to_coord:
                    search_queue.put((time_to_coord, ((new_x, new_y), new_equip)))
                    current_coord_dict[(new_x, new_y)] = time_to_coord
                    # aaa(new_x, new_y, current_coord_dict, time_to_coord, new_equip, search_queue)
                    print(new_x, new_y)
        if (x, y) == (target_x, target_y):

            for k, v in equip_time_coord_dicts["torch"].items():
                print(k, v)
            print()
            for k, v in equip_time_coord_dicts["neither"].items():
                print(k, v)
            print()
            for k, v in equip_time_coord_dicts["climbing gear"].items():
                print(k, v)
            print()
            if current_equip == "torch":
                return current_time
            return current_time + 7


def main():
    with open("22-ModeMaze-Input.txt") as input_file:
        cave_data = input_file.readlines()
    depth, x, y = parse_cave_input(cave_data)
    print(depth, x, y)
    cave = build_cave_2d_array(x, y)
    get_location_index_for_all_locations(cave, depth, x, y)
    erosion_map = build_erosion_map(cave, depth)
    for sublist in erosion_map:
        for element in sublist:
            print(element, end="")
        print()
    minimal_erosion_map = [sublist[:x+1] for sublist in erosion_map[:y+1]]
    risk_level = get_risk_level(minimal_erosion_map)
    print(risk_level)

    minimal_time = modified_search(erosion_map, x, y)
    print(minimal_time)


if __name__ == "__main__":
    main()
