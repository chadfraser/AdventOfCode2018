class LinkedList:
    def __init__(self, value):
        self.value = value
        self.previous_link = self
        self.next_link = self

    def insert_element_after_parameter_link(self, parameter_link):
        self.next_link = parameter_link.next_link
        self.previous_link = parameter_link
        parameter_link.next_link = self
        self.next_link.previous_link = self

    def delete_element(self):
        self.previous_link.next_link = self.next_link
        self.next_link.previous_link = self.previous_link

    def get_element_n_links_back(self, n):
        if n == 0:
            return self
        return self.previous_link.get_element_n_links_back(n-1)


def play_marble_game(player_count, final_value):
    player_scores = [0 for __ in range(player_count)]
    current_link = LinkedList(0)
    turn_count = 1

    while turn_count < final_value:
        if turn_count % 23 == 0:
            target_link = current_link.get_element_n_links_back(7)
            current_link = target_link.next_link
            target_link.delete_element()
            current_score = turn_count + target_link.value

            turn_player = (turn_count - 1) % player_count
            player_scores[turn_player] += current_score

        else:
            new_link = LinkedList(turn_count)
            target_link = current_link.next_link
            new_link.insert_element_after_parameter_link(target_link)
            current_link = new_link
        turn_count += 1

    return max(player_scores)


def get_values_from_string(data_string):
    data_list = data_string.split()
    player_count = int(data_list[0])
    final_score = int(data_list[6])
    return player_count, final_score


def main():
    with open("09-MarbleMania-Input.txt") as input_file:
        marble_data_string = input_file.readlines()[0]

    player_count, final_score = get_values_from_string(marble_data_string)
    print(player_count, final_score)

    high_score = play_marble_game(player_count, final_score)
    print(high_score)

    high_score = play_marble_game(player_count, final_score * 100)
    print(high_score)


if __name__ == "__main__":
    main()
