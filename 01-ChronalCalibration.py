def sum_list_of_values(list_of_values):
    """Given a list of ints, returns the total sum of those ints

    :param list_of_values: The list of ints we want to sum
    :return: The total sum of all ints in our list
    """
    total_sum = 0
    for value in list_of_values:
        total_sum += value
    return total_sum


def find_first_repeated_sum(list_of_values):
    """Given a list of ints, sum every int in turn and store that sum.
    Then, return once we reach a sum that we've already stored.
    If we reach the end of list without reaching any sum that we've already stored, restart from the beginning of the
    list again without resetting our sum to 0.

    :param list_of_values: The list of ints we want to sum
    :return: The first repeated sum we reach by iteratively summing the ints in our list
    """
    total_sum = 0
    found_sums = set()

    while True:
        for value in list_of_values:
            total_sum += value
            if total_sum in found_sums:
                return total_sum
            found_sums.add(total_sum)


def main():
    with open("01-ChronalCalibration-Input.txt") as input_file:
        list_of_ints = input_file.readlines()
    for num, current_int in enumerate(list_of_ints):
            list_of_ints[num] = int(current_int.strip())

    file_sum = sum_list_of_values(list_of_ints)
    print(file_sum)

    first_repeated_sum = find_first_repeated_sum(list_of_ints)
    print(first_repeated_sum)


if __name__ == "__main__":
    main()
