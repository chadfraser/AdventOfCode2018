import numpy as np


class CellMap:
    def __init__(self, serial_number):
        self.serial_number = serial_number
        self.cell_array = np.array([[0 for __ in range(300)] for __ in range(300)])

    def set_cell_power(self, x, y):
        rack_id = x + 10
        power_level = rack_id * y
        power_level += self.serial_number
        power_level *= rack_id
        power_level = power_level // 100 % 10
        power_level -= 5
        self.cell_array[y, x] = power_level

    def set_power_of_all_cells(self):
        for y_index, sub_array in enumerate(self.cell_array):
            for x_index, value in enumerate(sub_array):
                self.set_cell_power(x_index, y_index)

    def find_max_power_grid(self, size=3):
        max_power = -float("inf")
        x_coord = 0
        y_coord = 0

        # for value in np.nditer(self.cell_array[:-size]):
        for y_index, sub_array in enumerate(self.cell_array[:-size]):
            for x_index, value in enumerate(sub_array[:-size]):
                current_power = np.sum(self.cell_array[y_index:y_index+size, x_index:x_index+size])

                if current_power > max_power:
                    max_power = current_power
                    x_coord = x_index
                    y_coord = y_index
        return max_power, (x_coord, y_coord)


class AugmentedCellMap(CellMap):
    def __init__(self, serial_number):
        super().__init__(serial_number)
        self.serial_number = serial_number
        self.cell_array = [[[0, 0] for __ in range(300)] for __ in range(300)]
        # self.cell_array = np.array([[(0, 0) for __ in range(300)] for __ in range(300)])

    def set_cell_power(self, x, y):
        rack_id = x + 10
        power_level = rack_id * y
        power_level += self.serial_number
        power_level *= rack_id
        power_level = power_level // 100 % 10
        power_level -= 5
        self.cell_array[y][x] = [power_level, 0]
        # self.cell_array[y, x] = (power_level, 0)

    def set_power_of_all_cells(self):
        for y_index, sub_array in enumerate(self.cell_array):
            for x_index, value in enumerate(sub_array):
                self.set_cell_power(x_index, y_index)

    def find_max_power_grid(self, size):
        max_power = -float("inf")
        x_coord = 0
        y_coord = 0

        sum_array = []
        for y_index, sub_array in enumerate(self.cell_array):
            sum = 0
            for x_index, value in enumerate(sub_array):
                if size > 1:
                    pass


        # for y_index, sub_array in enumerate(self.cell_array[:-size]):
        #     for x_index, value in enumerate(sub_array[:-size]):
        #         if size > 1:
        #             current_power = self.cell_array[y_index][x_index][1]
        #             # print(current_power)
        #             current_power += sum(self.cell_array[i][x_index+size-1][0] for i in range(y_index, y_index+size))
        #             # for i in range(y_index, y_index + size):
        #             #     print(self.cell_array[i][x_index + size][0], i, x_index+size)
        #             # print(current_power)
        #             current_power += sum(self.cell_array[y_index+size-1][j][0] for j in range(x_index, x_index+size-1))
        #             # print(current_power)
        #             # input()
        #         else:
        #             current_power = sum(self.cell_array[i][j][0] for i in range(y_index, y_index+size)
        #                                 for j in range(x_index, x_index+size))
        #         self.cell_array[y_index][x_index][1] = current_power
        #
        #         if current_power > max_power:
        #             max_power = current_power
        #             x_coord = x_index
        #             y_coord = y_index

        # for i in range(6):
        #     for j in range(6):
        #         print(self.cell_array[i][j], end="")
        #     print()
        # input()
        return max_power, (x_coord, y_coord)

    def find_max_power_grid_of_any_size(self):
        max_power = -float("inf")
        best_coordinates = (0, 0)
        max_size = 0

        for size in range(1, 301):
            current_power, coordinates = self.find_max_power_grid(size)
            if current_power > max_power:
                print(f"new max: {current_power}, {size}")
                max_power = current_power
                best_coordinates = coordinates
                max_size = size
            print(size)
        return max_power, best_coordinates, max_size


def main():
    power_cells = CellMap(18)
    power_cells.set_power_of_all_cells()
    power_level, coordinates = power_cells.find_max_power_grid()
    print(coordinates)

    power_cells = AugmentedCellMap(18)
    power_cells.set_power_of_all_cells()
    # for i in range(6):
    #     for j in range(6):
    #         print(power_cells.cell_array[i][j], end="")
    #     print()
    # input()
    power_level, coordinates, size = power_cells.find_max_power_grid_of_any_size()
    print(power_level, coordinates, size)

    power_cells = CellMap(42)
    power_cells.set_power_of_all_cells()
    power_level, coordinates = power_cells.find_max_power_grid()
    print(coordinates)

    # power_cells = CellMap(42)
    # power_cells.set_power_of_all_cells()
    # power_level, coordinates, size = power_cells.find_max_power_grid_of_any_size()
    # print(power_level, coordinates, size)

    power_cells = CellMap(9221)
    power_cells.set_power_of_all_cells()
    power_level, coordinates = power_cells.find_max_power_grid()
    print(coordinates)

    power_cells = CellMap(9221)
    power_cells.set_power_of_all_cells()
    power_level, coordinates, size = power_cells.find_max_power_grid_of_any_size()
    print(coordinates, size)


# def kadane(list_to_search):
#     max_current = max_total = list_to_search[0]
#     first_index = last_index = 0
#
#     for index, value in enumerate(list_to_search[1:]):
#         if value > max_current + value:
#             first_index = index
#             max_current = value
#         else:
#             max_current = max_current + value
#         if max_current > max_total:
#             max_total = max_current
#             last_index = index
#     return max_total, first_index, last_index
#
#
# def kadane_2d(list_to_search):
#     left = right = top = bottom = 0
#     first_index = last_index = 0
#     max_current = max_total = -float("inf")
#
#     for left_index, sublist in enumerate(list_to_search):
#         temp_list = []
#         for right_index, value in enumerate(list_to_search[left_index:], left_index):
#             for num, sublist_value in enumerate(list_to_search):
#                 temp_list[num] += sublist_value[right_index]
#             max_current, current_first, current_last = kadane(temp_list)
#             if max_current[0] > max_total:
#                 max_total = max_current[0]
#                 left = left_index
#                 right = right_index
#                 top = current_first
#                 bottom = current_last
#     return max_total, left, right, top, bottom


if __name__ == "__main__":
    main()
