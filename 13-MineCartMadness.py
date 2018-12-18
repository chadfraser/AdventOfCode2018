from enum import Enum


class Directions(Enum):
    DOWN = "down"
    UP = "up"
    LEFT = "left"
    RIGHT = "right"
    STRAIGHT = "straight"


class AsciiMap:
    def __init__(self, map_coords_dict):
        self.crash_locations = []
        self.map_coords_dict = map_coords_dict
        self.number_of_carts = len(self.map_coords_dict.setdefault("v", [])) + \
                               len(self.map_coords_dict.setdefault("^", [])) + \
                               len(self.map_coords_dict.setdefault(">", [])) + \
                               len(self.map_coords_dict.setdefault("<", []))

        self.carts = []
        for coordinate in self.map_coords_dict["v"]:
            self.carts.append(Cart(Directions.DOWN, coordinate))
        for coordinate in self.map_coords_dict["^"]:
            self.carts.append(Cart(Directions.UP, coordinate))
        for coordinate in self.map_coords_dict["<"]:
            self.carts.append(Cart(Directions.LEFT, coordinate))
        for coordinate in self.map_coords_dict[">"]:
            self.carts.append(Cart(Directions.RIGHT, coordinate))
        self.set_up_map_coords_dict()
        self.sort_carts()

    def set_up_map_coords_dict(self):
        self.map_coords_dict.setdefault("|", []).extend(self.map_coords_dict["v"])
        self.map_coords_dict.setdefault("|", []).extend(self.map_coords_dict["^"])
        self.map_coords_dict.setdefault("-", []).extend(self.map_coords_dict["<"])
        self.map_coords_dict.setdefault("-", []).extend(self.map_coords_dict[">"])
        self.map_coords_dict.setdefault("+", [])
        self.map_coords_dict.setdefault("/", [])
        self.map_coords_dict.setdefault("\\", [])
        del self.map_coords_dict["v"]
        del self.map_coords_dict["^"]
        del self.map_coords_dict["<"]
        del self.map_coords_dict[">"]

    def move_carts(self):
        for cart in self.carts:
            if cart.coordinates in self.map_coords_dict["+"]:
                cart.choose_path_at_crossroads()
            elif cart.coordinates in self.map_coords_dict["/"]:
                cart.take_corner("/")
            elif cart.coordinates in self.map_coords_dict["\\"]:
                cart.take_corner("\\")
            cart.move()
            if self.check_for_crash():
                # print(f"Crash occurs at {self.get_crash_coordinates()}")
                self.remove_crashed_carts()
        self.sort_carts()

    def sort_carts(self):
        self.carts.sort(key=lambda cart: cart.coordinates)

    def remove_crashed_carts(self):
        crash_location = self.get_crash_coordinates()
        self.crash_locations.append(crash_location)

        new_carts_list = []
        for cart in self.carts:
            if cart.coordinates != crash_location:
                new_carts_list.append(cart)
        self.carts = new_carts_list
        self.number_of_carts = len(self.carts)

    def check_for_crash(self):
        set_of_cart_locations = set()
        for cart in self.carts:
            set_of_cart_locations.add(cart.coordinates)
        return len(set_of_cart_locations) < self.number_of_carts

    def get_crash_coordinates(self):
        set_of_all_cart_coordinates = set()
        for cart in self.carts:
            if cart.coordinates in set_of_all_cart_coordinates:
                return cart.coordinates
            set_of_all_cart_coordinates.add(cart.coordinates)

    def move_carts_until_crash(self):
        carts_total = self.number_of_carts
        while self.number_of_carts == carts_total:
            self.move_carts()

    def move_carts_until_all_crash(self):
        while len(self.carts) > 1:
            self.move_carts()


class Cart:
    def __init__(self, facing_direction, coordinates):
        self.facing_direction = facing_direction
        self.turning_direction = Directions.LEFT
        self.coordinates = coordinates

    def move(self):
        if self.facing_direction == Directions.DOWN:
            self.coordinates = (self.coordinates[0], self.coordinates[1] + 1)
        elif self.facing_direction == Directions.UP:
            self.coordinates = (self.coordinates[0], self.coordinates[1] - 1)
        elif self.facing_direction == Directions.LEFT:
            self.coordinates = (self.coordinates[0] - 1, self.coordinates[1])
        else:
            self.coordinates = (self.coordinates[0] + 1, self.coordinates[1])

    def take_corner(self, corner_character):
        if self.facing_direction == Directions.DOWN:
            if corner_character == "/":
                self.facing_direction = Directions.LEFT
            else:
                self.facing_direction = Directions.RIGHT
        elif self.facing_direction == Directions.UP:
            if corner_character == "/":
                self.facing_direction = Directions.RIGHT
            else:
                self.facing_direction = Directions.LEFT
        elif self.facing_direction == Directions.LEFT:
            if corner_character == "/":
                self.facing_direction = Directions.DOWN
            else:
                self.facing_direction = Directions.UP
        else:
            if corner_character == "/":
                self.facing_direction = Directions.UP
            else:
                self.facing_direction = Directions.DOWN

    def choose_path_at_crossroads(self):
        if self.turning_direction == Directions.LEFT:
            if self.facing_direction == Directions.DOWN:
                self.facing_direction = Directions.RIGHT
            elif self.facing_direction == Directions.UP:
                self.facing_direction = Directions.LEFT
            elif self.facing_direction == Directions.LEFT:
                self.facing_direction = Directions.DOWN
            else:
                self.facing_direction = Directions.UP

        elif self.turning_direction == Directions.RIGHT:
            if self.facing_direction == Directions.DOWN:
                self.facing_direction = Directions.LEFT
            elif self.facing_direction == Directions.UP:
                self.facing_direction = Directions.RIGHT
            elif self.facing_direction == Directions.LEFT:
                self.facing_direction = Directions.UP
            else:
                self.facing_direction = Directions.DOWN
        self.update_turning_direction()

    def update_turning_direction(self):
        if self.turning_direction == Directions.LEFT:
            self.turning_direction = Directions.STRAIGHT
        elif self.turning_direction == Directions.STRAIGHT:
            self.turning_direction = Directions.RIGHT
        else:
            self.turning_direction = Directions.LEFT


def convert_map_to_coordinates_dict(mine_cart_map):
    coordinates_dict = {}
    for y_value, line in enumerate(mine_cart_map):
        for x_value, character in enumerate(line.strip("\n")):
            coordinates_dict.setdefault(character, []).append((x_value, y_value))
    return coordinates_dict


def main():
    with open("13-MineCartMadness-Input.txt") as input_file:
        mine_cart_map = input_file.readlines()

    coordinates_dict = convert_map_to_coordinates_dict(mine_cart_map)

    ascii_map = AsciiMap(coordinates_dict)
    ascii_map.move_carts_until_crash()

    crash_coordinates = ascii_map.crash_locations[0]
    print(crash_coordinates)

    ascii_map.remove_crashed_carts()
    ascii_map.move_carts_until_all_crash()
    try:
        final_cart_coordinates = ascii_map.carts[0].coordinates
        print(final_cart_coordinates)
    except IndexError:
        print("No carts remain uncrashed.")


if __name__ == "__main__":
    main()
