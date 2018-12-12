from string import ascii_lowercase


def remove_repeated_letters_with_opposite_case(given_string, previous_index):
    """Given a string a multiple letters in both lower and uppercase, finds the first consecutive pair of letters of
     opposite case and returns a string identical to the given string with those letters removed.

    :param given_string: The string from which we want to remove repeated letters of opposite case
    :param previous_index: The index at which we found a repeated letters of opposite case the last time we called this
                           method
    :return: The given string with the first consecutive pair of letters of opposite case omitted,
    """

    # To prevent IndexErrors, we set a minimum value of 1 for previous_index
    previous_index = max(previous_index, 1)
    index = previous_index
    for index, char in enumerate(given_string[previous_index - 1 : -1], start=previous_index - 1):
        following_char = given_string[index + 1]
        if char.isupper() == following_char.islower() and char.upper() == following_char.upper():
            try:
                new_string = given_string[:index] + given_string[index + 2:]
                return new_string, index
            except IndexError:
                new_string = given_string[:index]
                return new_string, index
    return given_string, index


def get_length_of_string_after_reacting(current_string):
    """Finds the length of a string after 'reacting' it (Iteratively removing all consecutive pairs of letters, one
     upper case and one lower case, until no such consecutive pairs exist in the string).

    :param current_string: The string we wish to react
    :return: The length of the string after reacting
    """
    previous_index = 0

    while True:
        previous_line = current_string
        current_string, previous_index = remove_repeated_letters_with_opposite_case(current_string, previous_index)
        if current_string == previous_line:
            break
    return len(current_string)


def find_letter_to_remove_for_shortest_reaction_length(initial_string):
    """Checks the length of each string after reacting it and removing all instances of each letter in turn, and
     returns the letter and length of the string that is shortest after reacting.

    :param initial_string: The string we wish to remove letters from and then react
    :return: The letter that we can remove all instances of to get the shortest string after reacting, and the length
             of that string
    """
    shortest_length = float('inf')
    letter_with_best_reaction = ""

    for letter in ascii_lowercase:
        current_line = initial_string.replace(letter, "").replace(letter.upper(), "")
        current_length = get_length_of_string_after_reacting(current_line)
        if current_length < shortest_length:
            shortest_length = current_length
            letter_with_best_reaction = letter
    return letter_with_best_reaction, shortest_length


if __name__ == "__main__":
    with open("05-AlchemicalReduction-Input.txt") as input_file:
        line = input_file.readline().strip()
        final_length = get_length_of_string_after_reacting(line)
        print(final_length)

        best_letter, best_final_length = find_letter_to_remove_for_shortest_reaction_length(line)
        print(best_final_length)
