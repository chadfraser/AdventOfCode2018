from collections import Counter


class IdCartesianPlane:
    def __init__(self, width, height, id_num):
        """Initializes the id_locations_plane and id_projected_region_sizes fields of our IdCartesianPlane.

        :param width: The total width of our id_locations_plane (+1 to account for index 0)
        :param height: The total height of our id_locations_plane (+1 to account for index 0)
        :param id_num: The length of our id_projected_region_sizes list (+1 to account for index 0)
        """
        self.id_locations_plane = [["0" for __ in range(height + 1)] for __ in range(width + 1)]
        self.flat_id_locations_plane = []
        self.id_projected_region_sizes = ["" for __ in range(id_num + 1)]

    def write_id_to_plane(self, x, y, width, height, id_num):
        """Writes the current ID number to the indices of id_locations_plane in the given dimensions.

        :param x: The x-value of our id_locations_plane that we start writing from
        :param y: The y-value of our id_locations_plane that we start writing from
        :param width: The width of our id_locations_plane that we write our ID number to
        :param height: The height of our id_locations_plane that we write our ID number to
        :param id_num: The ID number we map to our plane
        """
        for vertical_val in range(y, y + height):
            for horizontal_val in range(x, x + width):
                if self.id_locations_plane[vertical_val][horizontal_val] == "0":
                    self.id_locations_plane[vertical_val][horizontal_val] = id_num

                # If we've already mapped a previous ID number to this index, we write an "X" to the index instead to
                # note this
                else:
                    self.id_locations_plane[vertical_val][horizontal_val] = "X"

    def store_id_region_size(self, width, height, id_num):
        """Notes the size of the ID's region (width * height) to the ID number's index in id_projected_region_sizes.

        :param width: The width of our ID number's region
        :param height: The height of our ID number's region
        :param id_num: The ID number of the region we store the size of
        """
        self.id_projected_region_sizes[id_num] = width * height

    def flatten_plane(self):
        """Writes the flat_id_locations_plane of this instance using the id_locations_plane.
        The id_locations_plane is a series of nested lists, while the flat_id_locations_plane is the same values in
        each of those nested lists, concatenated into a single list.
        """
        for sub_list in self.id_locations_plane:
            for value in sub_list:
                self.flat_id_locations_plane.append(value)

    def count_overlapping_ids(self):
        """Counts how many of our ID numbers' coordinates belong to multiple ID numbers at once (Representing by an "X"
        at that index in our id_locations_plane).
        We iterate across flat_id_locations_plane as opposed to fabric_map to prevent needing a nested for loop.

        :return: The amount of coordinates that overlap each other
        """
        overlaps = 0
        for value in self.flat_id_locations_plane:
            if value == "X":
                overlaps += 1
        return overlaps

    def find_first_id_without_overlaps(self):
        """Finds the first ID number whose coordinates do not overlap the coordinates of any other ID number.
        Makes use of the fact that any overlapping coordinates are rewritten as an "X", decreasing the coordinates
        written as that ID number by 1 (which means that the total number of coordinates written as that ID number will
        be less than the projected count for that ID number).

        :return: The first ID number that doesn't overlap any other ID numbers' coordinates
        """
        id_location_counter = Counter(self.flat_id_locations_plane)
        for id_num, size in enumerate(self.id_projected_region_sizes):
            if size == id_location_counter[id_num]:
                return id_num


def find_min_required_dimensions_for_id_plane(list_of_instructions):
    """Finds the minimum required width and height we need our IdCartesianPlane instance to be in order to take all of
    the measurements from our file.

    :param list_of_instructions: The list of ID numbers, coordinates, and dimensions we need to measure in our
                                 IdCartesianPlane
    :return: The minimum width and height our IdCartesianPlane needs to be, and the last ID number in our list
    """
    minimum_required_width = 0
    minimum_required_height = 0

    for instruction_sublist in list_of_instructions:
        __, x, y, width, height = instruction_sublist

        if x + width > minimum_required_width:
            minimum_required_width = x + width
        if y + height > minimum_required_height:
            minimum_required_height = y + height

    id_num = list_of_instructions[-1][0]
    return minimum_required_width, minimum_required_height, id_num


def add_id_to_cartesian_plane(list_of_instructions, cartesian_plane):
    """Maps the ID number of every instruction in our list to the id_locations_plane field in our cartesian_plane.

    :param list_of_instructions: The list of ID numbers, coordinates, and dimensions we need to map in our
                                 cartesian_plane
    :param cartesian_plane: The IdCartesianPlane instance that we map our IDs to
    """
    for instruction_sublist in list_of_instructions:
        id_num, x, y, width, height = instruction_sublist
        cartesian_plane.write_id_to_plane(x, y, width, height, id_num)
        cartesian_plane.store_id_region_size(width, height, id_num)


def format_instructions(raw_list_of_instructions):
    """Formats a raw list of strings of the format <ID __ X,Y: WIDTHxHEIGHT> into a list of lists of ints.

    :param raw_list_of_instructions: A list of strings, each one including an ID number, set of coordinates, and set of
                                     dimensions
    :return: A formatted list of lists, each including ints for an ID number x-coordinate, y-coordinate, width, and
             height
    """
    formatted_list_of_instructions = []
    for instruction in raw_list_of_instructions:
        id_num, __, coordinates, dimensions = instruction.split()
        id_num = int(id_num[1:])

        x, y = coordinates.strip(":").split(",")
        x = int(x)
        y = int(y)

        width, height = dimensions.split("x")
        width = int(width)
        height = int(height)
        formatted_list_of_instructions.append([id_num, x, y, width, height])
    return formatted_list_of_instructions


def main():
    with open("03-NoMatterHowYouSliceIt-Input.txt") as input_file:
        measurement_list = input_file.readlines()
    formatted_measurements = format_instructions(measurement_list)

    max_width, max_height, last_id_num = find_min_required_dimensions_for_id_plane(formatted_measurements)
    print(max_width, max_height, last_id_num)

    fabric = IdCartesianPlane(max_width, max_height, last_id_num)

    add_id_to_cartesian_plane(formatted_measurements, fabric)
    fabric.flatten_plane()
    fabric_overlaps = fabric.count_overlapping_ids()
    print(fabric_overlaps)

    id_without_overlaps = fabric.find_first_id_without_overlaps()
    print(id_without_overlaps)


if __name__ == "__main__":
    main()
