from collections import Counter


def sort_input_lines(file):
    """Sorts and returns the lines of the file parameter.

    :param file: The text file that we wish to sort
    :return: The list of sorted lines from the input file
    """
    input_lines = file.readlines()
    input_lines.sort()
    return input_lines


def track_sleeping_amount(sleep_dict, guard, sleep_time, wake_time):
    """Updates a dictionary with guard ID numbers as keys, and minutes that that guard spent asleep as values.

    :param sleep_dict: The current dictionary of minutes that guards have spent asleep
    :param guard: The current guard ID number to track the sleeping minutes of
    :param sleep_time: The time the current guard fell asleep
    :param wake_time: The time the current guard woke up
    :return: The updated dictionary of minutes that guards have spent asleep
    """
    sleep_dict.setdefault(guard, [])
    for num in range(sleep_time, wake_time):
        sleep_dict[guard].append(num)
    return sleep_dict


def get_guard_sleeping_minutes(sorted_data):
    """Parses data from the sorted list parameter to build a dictionary tracking the minutes that all guards have spent
    asleep.

    :param sorted_data: A sorted list of data tracking the date and time that guards started their shifts, fell asleep,
                        or woke up
    :return: A dictionary of all minutes that guards have spent asleep
    """
    current_guard_number = 0
    sleeping_minute = 0
    guard_data_dict = {}

    for line in sorted_data:
        date, time, instruction = line.split(" ", maxsplit=2)
        if instruction[0:5] == "Guard":
            __, guard_number, __ = instruction.split(" ", maxsplit=2)
            current_guard_number = int(guard_number[1:])
        elif instruction[0:5] == "falls":
            __, sleeping_minute = time.strip("]").split(":")
            sleeping_minute = int(sleeping_minute)
        else:
            __, waking_minute = time.strip("]").split(":")
            waking_minute = int(waking_minute)
            guard_data_dict = track_sleeping_amount(guard_data_dict, current_guard_number, sleeping_minute,
                                                    waking_minute)
    return guard_data_dict


def find_sleepiest_guard(sleep_dict):
    """Finds the guard that spent more minutes asleep than any other guard.

    :param sleep_dict: A dictionary of all minutes that guards have spent asleep
    :return: The ID number of the sleepiest guard
    """
    longest_sleeping_minutes = 0
    sleepiest_guard = ""

    for guard, minutes in sleep_dict.items():
        if len(minutes) > longest_sleeping_minutes:
            longest_sleeping_minutes = len(minutes)
            sleepiest_guard = guard
    return sleepiest_guard


def find_most_consistent_guard(sleep_dict):
    """Finds the guard that spent the same minute asleep more often than any other guard.

    :param sleep_dict: A dictionary of all minutes that guards have spent asleep
    :return: The ID number of the most consistent guard
    """
    most_frequent_sleeps = 0
    most_consistent_guard = ""

    for guard, minutes in sleep_dict.items():
        minute_counts = Counter(minutes)
        __, max_amount_of_sleeps = minute_counts.most_common(1)[0]
        if max_amount_of_sleeps > most_frequent_sleeps:
            most_frequent_sleeps = max_amount_of_sleeps
            most_consistent_guard = guard
    return most_consistent_guard


def find_most_common_minute(sleep_dict, chosen_guard):
    """Finds the most common minute in the sleep dict for a specific guard's ID number.

    :param sleep_dict: A dictionary of all minutes that guards have spent asleep
    :param chosen_guard: The ID number of the guard of who we want to find the most common minute they spent asleep
    :return: The most common minute that the chosen guard spends asleep
    """
    minute_counts = Counter(sleep_dict[chosen_guard])
    most_common_minute, __ = minute_counts.most_common(1)[0]
    return most_common_minute


if __name__ == "__main__":
    with open("04-ReposeRecord-Input.txt") as input_file:
        sorted_file_data = sort_input_lines(input_file)
        sleeping_minutes_dict = get_guard_sleeping_minutes(sorted_file_data)

        guard_to_pick = find_sleepiest_guard(sleeping_minutes_dict)
        minute_to_pick = find_most_common_minute(sleeping_minutes_dict, guard_to_pick)
        print(guard_to_pick, minute_to_pick, guard_to_pick * minute_to_pick)

        guard_to_pick = find_most_consistent_guard(sleeping_minutes_dict)
        minute_to_pick = find_most_common_minute(sleeping_minutes_dict, guard_to_pick)
        print(guard_to_pick, minute_to_pick, guard_to_pick * minute_to_pick)
