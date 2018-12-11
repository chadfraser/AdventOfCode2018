from collections import Counter


def count_repeated_letters(file):
    doubles = 0
    triples = 0
    for line in file:
        counted_line = Counter(line.strip())
        if 2 in counted_line.values():
            doubles += 1
        if 3 in counted_line.values():
            triples += 1
    print(doubles, triples, doubles * triples)


def find_similar_strings(file):
    list_of_checked_lines = []
    for line in file:
        for item in list_of_checked_lines:
            if compare_differences_in_strings(line.strip(), item):
                print(line.strip(), item)
                for line_char, item_char in zip(line, item):
                    if line_char == item_char:
                        print(line_char, end="")
                return
        list_of_checked_lines.append(line.strip())


def compare_differences_in_strings(line, item):
    differences = 0
    for line_char, item_char in zip(line, item):
        if line_char != item_char:
            differences += 1
            if differences > 1:
                return False
    return True


with open("02-InventoryManagementSystem-Input.txt") as input_file:
    count_repeated_letters(input_file)
    input_file.seek(0)
    find_similar_strings(input_file)
