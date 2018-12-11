def sum_input_file(file):
    total_sum = 0
    for line in file:
        total_sum += int(line.strip())
    print(total_sum)


def find_first_repeated_sum(file):
    total_sum = 0
    found_sums = set()
    while True:
        for line in file:
            total_sum += int(line.strip())
            if total_sum in found_sums:
                print(total_sum)
                return total_sum
            found_sums.add(total_sum)
        input_file.seek(0)


with open("01-ChronalCalibration-Input.txt") as input_file:
    sum_input_file(input_file)
    input_file.seek(0)
    find_first_repeated_sum(input_file)
