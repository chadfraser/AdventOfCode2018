from collections import deque


class Room:
    def __init__(self):
        self.north = None
        self.east = None
        self.south = None
        self.west = None

    def add_room(self, key, room):
        if key == "N":
            self.north = room
            room.south = self
        elif key == "E":
            self.east = room
            room.west = self
        elif key == "S":
            self.south = room
            room.north = self
        else:
            self.west = room
            room.east = self


def build_map(regex_data):
    current_coords = (0, 0)
    first_room = current_room = Room()
    room_coords = {(0, 0): current_room}
    stored_room = []
    for character in regex_data:
        if character in "NESW":
            if character == "N":
                current_coords = (current_coords[0], current_coords[1] - 1)
            elif character == "E":
                current_coords = (current_coords[0] + 1, current_coords[1])
            elif character == "S":
                current_coords = (current_coords[0], current_coords[1] + 1)
            else:
                current_coords = (current_coords[0] - 1, current_coords[1])
            if current_coords in room_coords:
                connected_room = room_coords[current_coords]
            else:
                connected_room = Room()
                room_coords[current_coords] = connected_room
            current_room.add_room(character, connected_room)
            current_room = connected_room

        elif character == "(":
            stored_room.append([current_room, current_coords])
        elif character == "|":
            current_room, current_coords = stored_room[-1]
        elif character == ")":
            current_room, current_coords = stored_room.pop()
    return current_room, room_coords


def get_room_distance(room_dict_data):
    current_room = room_dict_data[(0, 0)]
    current_door_count = 0
    rooms_to_map = deque([(current_room, current_door_count)])
    rooms_visited = {current_room}
    room_distance = {(current_room, current_door_count)}
    while rooms_to_map:
        current_room, current_door_count = rooms_to_map.popleft()
        for room in [current_room.north, current_room.east, current_room.south, current_room.west]:
            if room and room not in rooms_visited:
                rooms_to_map.append((room, current_door_count + 1))
                rooms_visited.add(room)
                room_distance.add((room, current_door_count + 1))
    return room_distance


def get_distance_of_furthest_room(room_distance):
    __, furthest_distance = max(room_distance, key=lambda x: x[1])
    return furthest_distance


def get_count_of_rooms_farther_than_passed_distance(room_distance, minimum_distance=1000):
    count = 0
    for room, distance in room_distance:
        if distance >= minimum_distance:
            count += 1
    return count


def main():
    with open("20-ARegularMap-Input.txt") as input_file:
        room_regex_data = input_file.readlines()[0][1:-1]
    __, room_coords = build_map(room_regex_data)
    distance_of_rooms = get_room_distance(room_coords)
    furthest_distance = get_distance_of_furthest_room(distance_of_rooms)
    print(furthest_distance)

    count_of_far_rooms = get_count_of_rooms_farther_than_passed_distance(distance_of_rooms)
    print(count_of_far_rooms)


if __name__ == "__main__":
    main()
