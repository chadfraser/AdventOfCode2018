from collections import Counter


class CoordinatesMap:
    def __init__(self, width, height, id_count):
        """Initializes the coord_map, distance_map, id_locations, and ids_of_infinite_size fields of our CoordinateMap
         instance.

        :param width: The total width of our coord_map and distance_map (+1 to account for index 0)
        :param height: The total height of our coord_map and distance_map (+1 to account for index 0)
        :param id_count: The length of our id_locations list (+1 to account for index 0)
        """
        self.coord_map = [[0 for __ in range(width + 1)] for __ in range(height + 1)]
        self.distance_map = [[0 for __ in range(width + 1)] for __ in range(height + 1)]
        self.id_locations = [(-1, -1) for __ in range(id_count + 1)]
        self.ids_of_infinite_size = {0}
        self.flat_coord_map = []

    def place_id_at_coordinates(self, x, y, id_num):
        """Places the ID number at the passed coordinates in the coord_map and updates the id_locations for that index.

        :param x: The x-coordinate to place our ID number at in our coord_map
        :param y: The y-coordinate to place our ID number at in our coord_map
        :param id_num: The ID number to place at the passed coordinates in our coord_map
        """
        self.coord_map[y][x] = id_num
        self.id_locations[id_num] = (x, y)

    def find_nearest_id_to_point(self, x, y):
        """Finds the ID number that is located the closest to the passed coordinates and updates those coordinates in
        our coord_map.
        If there are multiple ID numbers located equally close to these coordinates, does not update them.

        :param x: The x-coordinate of the point
        :param y: The y-coordinate of the point
        """
        minimum_distance_to_id = float("inf")
        nearest_id = None

        for id_num, (id_x, id_y) in enumerate(self.id_locations[1:], 1):
            distance = abs(x - id_x) + abs(y - id_y)
            if distance == minimum_distance_to_id:
                nearest_id = None
            elif distance < minimum_distance_to_id:
                minimum_distance_to_id = distance
                nearest_id = id_num
        if nearest_id is not None:
            self.coord_map[y][x] = nearest_id

    def map_nearest_id_for_all_points(self):
        """Update the coord_map with the nearest ID number for every point in the map."""
        for vertical_index, sublist in enumerate(self.coord_map):
            for horizontal_index, value in enumerate(sublist):
                if value == 0:
                    self.find_nearest_id_to_point(horizontal_index, vertical_index)

    def find_ids_of_infinite_size(self):
        """Places all ID numbers that encompass a (simulated) region of infinite size into our ids_of_infinite_size
        set.
        These ID numbers are those on the edges of our coordinates map, since they can be thought of as extending
        infinitely in those directions.
        """
        for val in self.coord_map[0]:
            if val not in self.ids_of_infinite_size:
                self.ids_of_infinite_size.add(val)
        for val in self.coord_map[-1]:
            if val not in self.ids_of_infinite_size:
                self.ids_of_infinite_size.add(val)
        for sublist in self.coord_map[1:-1]:
            for val in (sublist[0], sublist[-1]):
                if val not in self.ids_of_infinite_size:
                    self.ids_of_infinite_size.add(val)

    def flatten_map(self):
        """Writes the flat_map of this instance using the coord_map.
        The coord_map is a series of nested lists, while the flat_map is the same values in each of those nested
        lists, concatenated into a single list.
        """
        for sub_list in self.coord_map:
            for value in sub_list:
                self.flat_coord_map.append(value)

    def get_maximum_finite_area(self):
        """Flattens the coord_map and then finds the count of all coordinates closest to ID x for all ID's, then
        returns the ID the has the largest finite area, and that area.

        :return: The ID that has the region with the largest finite area in our coord_map, and the area of that ID's
                 region.
        """
        self.flatten_map()
        id_counts = Counter(self.flat_coord_map)
        most_common_ids = id_counts.most_common()
        current_id_index = 0
        maximum_val = most_common_ids[0][0]

        while maximum_val in self.ids_of_infinite_size:
            current_id_index += 1
            maximum_val = most_common_ids[current_id_index][0]
        return maximum_val, id_counts[maximum_val]

    def find_cumulative_distance_from_all_ids_to_point(self, x, y):
        """Finds the cumulative distance from every ID number to the passed coordinates and updates that distance in
        our distance_map.

        :param x: The x-coordinate of the point
        :param y: The y-coordinate of the point
        """
        distance = 0
        for id_num, (id_x, id_y) in enumerate(self.id_locations[1:], 1):
            distance += abs(x - id_x) + abs(y - id_y)
        self.coord_map[y][x] = distance

    def find_cumulative_distance_for_all_points(self):
        """Update the distance_map with the cumulative distance to every ID number for every point in the map."""
        for vertical_index, sublist in enumerate(self.coord_map):
            for horizontal_index, value in enumerate(sublist):
                self.find_cumulative_distance_from_all_ids_to_point(horizontal_index, vertical_index)

    def get_size_of_region_within_range_of_ids(self):
        """Finds the total number of points in our map within 10000 spaces of all ID numbers, cumulatively, then
        returns this value.

        :return: The number of points within 1000 spaces of all ID numbers
        """
        region_size = 0
        for vertical_index, sublist in enumerate(self.coord_map):
            for horizontal_index, value in enumerate(sublist):
                if value < 10000:
                    region_size += 1
        return region_size


def get_maximum_dimensions_and_id_of_file(file):
    """Finds the maximum width and height any ID will be located at, and the total number of ID coordinates in our
    file.

    :param file: The file containing ID coordinates
    :return: The maximum x-value and y-value coordinates in any of our ID coordinates, and the total number of ID
             coordinates in our file
    """
    max_x = 0
    max_y = 0
    id_num = 0
    for line in file:
        id_num += 1

        x, y = line.strip().split()
        x = int(x[:-1])
        y = int(y)
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
    return max_x, max_y, id_num


def place_coordinates_from_file_to_map(file, coordinates_instance):
    """Places the ID numbers from every line in our file to the appropriate coordinates in our coord_map.

    :param file: The file containing the ID numbers and coordinates we want to map
    :param coordinates_instance: The CoordinatesMap instance which will map the IDs from our file
    """
    for line_num, line in enumerate(file, 1):
        x, y = line.strip().split()
        x = int(x[:-1])
        y = int(y)
        coordinates_instance.place_id_at_coordinates(x, y, line_num)


if __name__ == "__main__":
    with open("06-ChronalCoordinates-Input.txt") as input_file:
        map_width, map_height, id_total = get_maximum_dimensions_and_id_of_file(input_file)
        input_file.seek(0)

        coordinates_map = CoordinatesMap(map_width, map_height, id_total)
        place_coordinates_from_file_to_map(input_file, coordinates_map)
        coordinates_map.map_nearest_id_for_all_points()
        coordinates_map.find_ids_of_infinite_size()
        id_of_largest_finite_area, size_of_largest_finite_area = coordinates_map.get_maximum_finite_area()
        print(id_of_largest_finite_area, size_of_largest_finite_area)

        coordinates_map.find_cumulative_distance_for_all_points()
        size_of_region_near_all_ids = coordinates_map.get_size_of_region_within_range_of_ids()
        print(size_of_region_near_all_ids)
