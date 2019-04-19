from collections import Counter


def count_doubled_and_tripled_letters(list_of_strings):
    """Finds the count of all letters in each string of our list.
    Returns the amount of strings that contain exactly two of one or more letter(s), and the amount of strings that
    contain exactly three of one or more letter(s).

    :param list_of_strings: The list of the strings that we want to count the repeated letters of
    :return: The amount of strings that contain exactly two/three of one or more letter(s)
    """
    doubles = 0
    triples = 0
    for current_string in list_of_strings:
        current_string_counter = Counter(current_string.strip())
        if 2 in current_string_counter.values():
            doubles += 1
        if 3 in current_string_counter.values():
            triples += 1
    return doubles, triples


def find_similar_strings(list_of_strings):
    """Finds the two strings in our list that differ by only one character in one position.

    :param list_of_strings: The list of all of the strings that we want to compare
    :return: The strings that differ by only one character in one position
    """
    list_of_checked_strings = []
    for current_string in list_of_strings:
        for string_to_compare in list_of_checked_strings:
            if strings_differ_by_one_character(current_string, string_to_compare):
                return current_string, string_to_compare
        list_of_checked_strings.append(current_string.strip())


def strings_differ_by_one_character(string_a, string_b):
    """Returns whether the two strings differ by only one or zero character(s).

    :param string_a: The first string that we want to compare
    :param string_b: The second string that we want to compare
    """
    return compare_differences_in_strings_to_maximum_amount(string_a, string_b, 1)


def compare_differences_in_strings_to_maximum_amount(string_a, string_b, maximum_desired_differences):
    """Compares all of the letters in two strings, returning whether or not those strings differ by at most
    maximum_desired_differences.

    :param string_a: The first string that we want to compare
    :param string_b: The second string that we want to compare
    :param maximum_desired_differences: The maximum amount of different characters we want in our string
    :return: A boolean saying if the two strings differ by fewer than the maximum amount of differences allowed
    """
    differences = 0
    for char_a, char_b in zip(string_a, string_b):
        if char_a != char_b:
            differences += 1
            if differences > maximum_desired_differences:
                return False
    return True


def get_shared_characters_string(string_a, string_b):
    """Finds the string made by removing all characters that differ in our two strings parameters.

    :param string_a: The first string that we want to compare
    :param string_b: The second string that we want to compare
    :return: The string made by removing all characters that differ in our two strings parameters
    """
    shared_string_list = [char_a for char_a, char_b in zip(string_a, string_b) if char_a == char_b]
    return "".join(shared_string_list)


def main():
    with open("02-InventoryManagementSystem-Input.txt") as input_file:
        list_of_id_codes = input_file.readlines()
    for num, id_code in enumerate(list_of_id_codes):
        list_of_id_codes[num] = id_code.strip()

    doubled_values, tripled_values = count_doubled_and_tripled_letters(list_of_id_codes)
    print(doubled_values, tripled_values, doubled_values * tripled_values)

    similar_string_a, similar_string_b = find_similar_strings(list_of_id_codes)
    print(similar_string_a, similar_string_b)

    similar_string_characters = get_shared_characters_string(similar_string_a, similar_string_b)
    print(similar_string_characters)


if __name__ == "__main__":
    main()
