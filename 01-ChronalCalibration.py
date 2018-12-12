def sum_input_file(file):
    """Given a file with an int on each line, returns the total sum of those ints

    :param file: The text file from which we take all of the ints we want to sum
    :return: The total sum of all ints in our file
    """
    total_sum = 0
    for line in file:
        total_sum += int(line.strip())
    return total_sum


def find_first_repeated_sum(file):
    """Given a file with an int on each line, sum every int in turn and store that sum.
    Then, return once we reach a sum that we've already stored.
    If we reach the end of file without reaching a sum that we've already stored, restart from the beginning of the
    file again without resetting our sum to 0.

    :param file: The text file from which we take all of the ints we want to sum
    :return: The sum
    """
    total_sum = 0
    found_sums = set()

    while True:
        for line in file:
            total_sum += int(line.strip())
            if total_sum in found_sums:
                return total_sum
            found_sums.add(total_sum)
        input_file.seek(0)


if __name__ == "__main__":
    with open("01-ChronalCalibration-Input.txt") as input_file:
        file_sum = sum_input_file(input_file)
        print(file_sum)

        input_file.seek(0)
        first_repeated_sum = find_first_repeated_sum(input_file)
        print(first_repeated_sum)
