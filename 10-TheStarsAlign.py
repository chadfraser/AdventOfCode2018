import re


def find_area_coordinates_span(coordinate_data):
    width = find_coordinates_width(coordinate_data)
    height = find_coordinates_height(coordinate_data)
    return width * height


def find_coordinates_height(coordinate_data):
    min_y = min(data[1] for data in coordinate_data)
    max_y = max(data[1] for data in coordinate_data)
    return max_y - min_y


def find_coordinates_width(coordinate_data):
    min_x = min(data[0] for data in coordinate_data)
    max_x = max(data[0] for data in coordinate_data)
    return max_x - min_x


def move_coordinate_points(coordinate_data, seconds):
    new_data_list = [(x + x_velocity, y + y_velocity, x_velocity, y_velocity) for
                     (x, y, x_velocity, y_velocity) in coordinate_data]
    seconds += 1
    return new_data_list, seconds


def reverse_coordinate_points(coordinate_data, seconds):
    new_data_list = [(x - x_velocity, y - y_velocity, x_velocity, y_velocity) for
                     (x, y, x_velocity, y_velocity) in coordinate_data]
    seconds -= 1
    return new_data_list, seconds


def parse_data(coordinates_lines):
    data_list = []
    for num, line in enumerate(coordinates_lines):
        __, x, y, __, x_velocity, y_velocity, __ = re.split("< |<|> |>|, ", line.strip())
        x = int(x)
        y = int(y)
        x_velocity = int(x_velocity)
        y_velocity = int(y_velocity)
        data_list.append((x, y, x_velocity, y_velocity))
    return data_list


def print_coordinate_data(coordinate_data):
    min_x = min(data[0] for data in coordinate_data)
    max_x = max(data[0] for data in coordinate_data)
    min_y = min(data[1] for data in coordinate_data)
    max_y = max(data[1] for data in coordinate_data)

    coordinates = [(x, y) for (x, y, x_velocity, y_velocity) in coordinate_data]

    for y_val in range(min_y, max_y+1):
        for x_val in range(min_x, max_x+1):
            if (x_val, y_val) in coordinates:
                print("#", end="")
            else:
                print(" ", end="")
        print()


def print_and_move_coordinates_until_done(coordinate_data, seconds):
    input_val = ""
    while not input_val:
        print("\n\n\n\n\n\n")
        coordinate_data, seconds = move_coordinate_points(coordinate_data, seconds)
        print_coordinate_data(coordinate_data)
        input_val = input()
    return seconds


def main():
    tolerance = 50
    seconds = 0

    with open("10-TheStarsAlign-Input.txt") as input_file:
        coordinates_lines = input_file.readlines()
    coordinate_data_list = parse_data(coordinates_lines)

    # coordinates_height = find_coordinates_height(coordinate_data_list)
    # while coordinates_height > tolerance:
    #     coordinate_data_list, seconds = move_coordinate_points(coordinate_data_list, seconds)
    #     coordinates_height = find_coordinates_height(coordinate_data_list)

    previous_size_of_data = find_area_coordinates_span(coordinate_data_list)
    coordinate_data_list, seconds = move_coordinate_points(coordinate_data_list, seconds)
    updated_size_of_data = find_area_coordinates_span(coordinate_data_list)
    while updated_size_of_data < previous_size_of_data:
        previous_size_of_data = updated_size_of_data
        coordinate_data_list, seconds = move_coordinate_points(coordinate_data_list, seconds)
        updated_size_of_data = find_area_coordinates_span(coordinate_data_list)
    coordinate_data_list, seconds = reverse_coordinate_points(coordinate_data_list, seconds)
    coordinate_data_list, seconds = reverse_coordinate_points(coordinate_data_list, seconds)

    seconds = print_and_move_coordinates_until_done(coordinate_data_list, seconds)
    print(seconds)


if __name__ == "__main__":
    main()
