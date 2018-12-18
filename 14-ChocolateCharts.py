# def sum_digits_in_a_number(number):
#     total_sum = 0
#     while number:
#         total_sum += number % 10
#         number //= 10
#     return total_sum


def add_recipe(index_of_first, index_of_second, chart):
    sum_of_scores = chart[index_of_first] + chart[index_of_second]
    if sum_of_scores >= 10:
        first_digit = sum_of_scores // 10
        last_digit = sum_of_scores % 10
        chart.append(first_digit)
        chart.append(last_digit)
    else:
        chart.append(sum_of_scores)
    return chart


def move_people(index_of_first, index_of_second, chart):
    value_of_first = chart[index_of_first] + 1
    value_of_second = chart[index_of_second] + 1
    first_move_position = (index_of_first + value_of_first) % len(chart)
    second_move_position = (index_of_second + value_of_second) % len(chart)
    return first_move_position, second_move_position


def main():
    index_of_first_person = 0
    index_of_second_person = 1
    chart_of_scores = [3, 7]

    with open("14-ChocolateCharts-Input.txt") as input_file:
        number_of_recipes = int(input_file.readlines()[0])

    while len(chart_of_scores) < number_of_recipes + 10:
        chart_of_scores = add_recipe(index_of_first_person, index_of_second_person, chart_of_scores)
        index_of_first_person, index_of_second_person = move_people(index_of_first_person, index_of_second_person,
                                                                    chart_of_scores)

    for char in chart_of_scores[number_of_recipes:number_of_recipes+10]:
        print(char, end="")
    print()

    string_representation = "".join(str(x) for x in chart_of_scores)
    while True:
        if str(number_of_recipes) in string_representation:
            print(string_representation.index(str(number_of_recipes)))
            break
        else:
            for __ in range(number_of_recipes):
                chart_of_scores = add_recipe(index_of_first_person, index_of_second_person, chart_of_scores)
                index_of_first_person, index_of_second_person = move_people(index_of_first_person,
                                                                            index_of_second_person, chart_of_scores)
            string_representation = "".join(str(x) for x in chart_of_scores)


if __name__ == "__main__":
    main()
