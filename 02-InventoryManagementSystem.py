from collections import Counter


def count_doubled_and_tripled_letters(file):
    """Finds the count of all letters in each line of our file.
    Stores and returns the amount of lines that contain exactly two of one or more letter(s), and the amount of lines
    that contain exactly three of one or more letter(s).

    :param file: The file from which we take all of the strings that we want to count the repeated letters of
    :return: The amount of lines that contain exactly two/three of one or more letter(s)
    """
    doubles = 0
    triples = 0
    for line in file:
        counted_line = Counter(line.strip())
        if 2 in counted_line.values():
            doubles += 1
        if 3 in counted_line.values():
            triples += 1
    return doubles, triples


def find_similar_strings(file):
    """Finds the two lines in our file that differ by only one character in one position.

    :param file: The file from which we take all of the strings that we want to compare
    :return: The lines that differ by only one character in one position
    """
    list_of_checked_lines = []
    for line in file:
        line = line.strip()
        for line_to_compare in list_of_checked_lines:
            if compare_differences_in_strings(line, line_to_compare):
                return line, line_to_compare
        list_of_checked_lines.append(line.strip())


def compare_differences_in_strings(string_a, string_b):
    """Compare all of the letters in two strings.
    Returns whether the two strings differ by only one or zero character(s)

    :param string_a: The first string that we want to compare
    :param string_b: The second string that we want to compare
    :return: A boolean saying if the two strings differ by only one or zero character(s)
    """
    differences = 0
    for char_a, char_b in zip(string_a, string_b):
        if char_a != char_b:
            differences += 1
            if differences > 1:
                return False
    return True


def get_shared_string_characters(string_a, string_b):
    """Finds the string made by removing all characters that differ in our two strings parameters.

    :param string_a: The first string that we want to compare
    :param string_b: The second string that we want to compare
    :return: The string made by removing all characters that differ in our two strings parameters
    """
    # shared_string = ""
    shared_string_list = [char_a for char_a, char_b in zip(string_a, string_b) if char_a == char_b]
    # for char_a, char_b in zip(string_a, string_b):
    #     if char_a == char_b:
    #         shared_string += char_a
    return "".join(shared_string_list)


if __name__ == "__main__":
    with open("02-InventoryManagementSystem-Input.txt") as input_file:
        doubled_values, tripled_values = count_doubled_and_tripled_letters(input_file)
        print(doubled_values, tripled_values, doubled_values * tripled_values)

        input_file.seek(0)
        similar_string_a, similar_string_b = find_similar_strings(input_file)
        print(similar_string_a, similar_string_b)

        similar_string_characters = get_shared_string_characters(similar_string_a, similar_string_b)
        print(similar_string_characters)
