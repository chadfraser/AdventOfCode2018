from collections import Counter


class FabricMap:
    def __init__(self, width, height, id_num):
        """Initializes the fabric_map and projected_dimensions fields of our FabricMap instance.

        :param width: The total width of our_fabric map (+1 to account for index 0)
        :param height: The total height of our_fabric map (+1 to account for index 0)
        :param id_num: The length of our dimension_sizes list
        """
        self.fabric_map = [["0" for __ in range(height + 1)] for __ in range(width + 1)]
        self.flat_fabric_map = []
        self.projected_dimensions = ["" for __ in range(id_num + 1)]

    def map_dimensions(self, x, y, width, height, id_num):
        """Writes the current ID number to the indices of fabric_map in the given measurements.
        Then, maps the size of each measurement (width * height) to the ID number's index in dimension_sizes.

        :param x: The x-value of our fabric_map that we start measuring from
        :param y: The y-value of our fabric_map that we start measuring from
        :param width: The required width of our current measurement
        :param height: The required height of our current measurement
        :param id_num: The ID number of the current measurement
        """
        for vertical_val in range(y, y + height):
            for horizontal_val in range(x, x + width):
                if self.fabric_map[vertical_val][horizontal_val] == "0":
                    self.fabric_map[vertical_val][horizontal_val] = id_num

                # If we've already mapped a previous ID number to this index, we write an "X" to the index instead to
                # note this
                else:
                    self.fabric_map[vertical_val][horizontal_val] = "X"
        self.projected_dimensions[id_num] = width * height

    def flatten_map(self):
        """Writes the flat_map of this instance using the fabric_map.
        The fabric_map is a series of nested lists, while the flat_map is the same values in each of those nested
        lists, concatenated into a single list.
        """
        for sub_list in self.fabric_map:
            for value in sub_list:
                self.flat_fabric_map.append(value)

    def count_overlaps(self):
        """Counts how many of our measurements' coordinates overlap each other (Representing by an "X" at that index in
        our fabric_map).
        We iterate across flat_fabric_map as opposed to fabric_map to prevent needing a nested for loop.

        :return: The amount of coordinates that overlap each other
        """
        overlaps = 0
        for value in self.flat_fabric_map:
            if value == "X":
                overlaps += 1
        return overlaps

    def find_id_without_overlaps(self):
        """Finds the first ID number whose measurements do not overlap the measurements of any other ID number.
        Makes use of the fact that any overlapping coordinates are rewritten as an "X", decreasing the coordinates
        written as that ID number by 1 (which means that the total number of coordinates written as that ID number will
        be less than the projected measurement for that ID number).

        :return: The first ID number that doesn't overlap any other ID number's measurements
        """
        fabric_counter = Counter(self.flat_fabric_map)
        for id_num, dimension in enumerate(self.projected_dimensions):
            if dimension == fabric_counter[id_num]:
                return id_num


def find_min_required_dimensions(file):
    """Finds the minimum required width and height we need our FabricMap instance to be in order to take all of the
    measurements from our file.

    :param file: The file containing the coordinates and dimensions we need to measure in our FabricMap instance
    :return: The minimum width and height our FabricMap instance needs to be
    """
    max_a = 0
    max_b = 0
    id_num = 0

    for line in file:
        id_num, __, coordinates, dimensions = line.split()
        x, y = (int(a) for a in coordinates.strip(":").split(","))
        width, height = (int(a) for a in dimensions.split("x"))
        if x + width > max_a:
            max_a = x + width
        if y + height > max_b:
            max_b = y + height
    id_num = int(id_num[1:])
    return max_a, max_b, id_num


def find_fabric_overlaps(file, fabric_instance):
    """Maps the ID number of every measurement in our file to the fabric_map field in our fabric_instance.
    Then, flattens the fabric_map of our fabric_instance and returns the total sum of coordinates that are a part of
    two or more measurements at once.

    :param file: The file containing the measurements we need to map in our fabric_instance
    :param fabric_instance: The FabricMap instance that we map our measurements to
    :return: The total sum of coordinates that are a part of two or more measurements at once
    """
    for line in file:
        id_num, __, coordinates, dimensions = line.split()
        id_num = int(id_num[1:])
        x, y = (int(a) for a in coordinates.strip(':').split(','))
        width, height = (int(a) for a in dimensions.split('x'))
        fabric_instance.map_dimensions(x, y, width, height, id_num)
    fabric_instance.flatten_map()
    return fabric_instance.count_overlaps()


if __name__ == "__main__":
    with open("03-NoMatterHowYouSliceIt-Input.txt") as input_file:
        max_width, max_height, last_id_num = find_min_required_dimensions(input_file)
        print(max_width, max_height, last_id_num)
        fabric = FabricMap(max_width, max_height, last_id_num)

        input_file.seek(0)
        fabric_overlaps = find_fabric_overlaps(input_file, fabric)
        print(fabric_overlaps)

        input_file.seek(0)
        id_without_overlaps = fabric.find_id_without_overlaps()
        print(id_without_overlaps)
