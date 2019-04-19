class Graph:
    def __init__(self):
        self.all_nodes = {}
        self.currently_accessible_nodes = {}

    def copy_node_sets_for_all_nodes(self):
        for node in self.all_nodes:
            node.store_copy_of_node_sets()

    def take_next_sorted_accessible_node_from_graph(self):
        accessible_nodes = sorted(self.currently_accessible_nodes)
        alphabetical_accessible_node = accessible_nodes[0]
        return self.currently_accessible_nodes[alphabetical_accessible_node]

    def get_next_node(self):
        node = self.take_next_sorted_accessible_node_from_graph()
        del self.currently_accessible_nodes[node.value]
        return node

    def update_currently_accessible_nodes(self, node):
        for following_node in node.following_nodes:
            following_node.preceding_nodes.remove(node)
            if len(following_node.preceding_nodes) == 0:
                self.currently_accessible_nodes[following_node.value] = following_node

    def get_all_nodes_in_order(self):
        ordered_nodes = []
        while self.currently_accessible_nodes:
            node = self.get_next_node()
            self.update_currently_accessible_nodes(node)
            ordered_nodes.append(node.value)
        return "".join(ordered_nodes)

    def swap_nodes_sets(self):
        for node in self.all_nodes:
            node.swap_sets()

    def work_on_nodes(self):
        nodes_being_worked_on = set()
        time_spent_working = 0

        while self.all_nodes:
            time_spent_working += 1
            new_node_set = set()
            while len(nodes_being_worked_on) < 5 and self.currently_accessible_nodes:
                nodes_being_worked_on.add(self.get_next_node())
            for node in nodes_being_worked_on:
                node.numeric_value -= 1
                if node.numeric_value == 0:
                    self.update_currently_accessible_nodes(node)
                    del self.all_nodes[node.value]
                else:
                    new_node_set.add(node)
            nodes_being_worked_on = new_node_set
        return time_spent_working


class Node:
    def __init__(self, value):
        self.value = value
        self.following_nodes = set()
        self.preceding_nodes = set()
        self.following_nodes_copy = set()
        self.preceding_nodes_copy = set()
        self.numeric_value = 60 + ord(value.lower()) - 96

    def store_copy_of_node_sets(self):
        self.following_nodes_copy = self.following_nodes.copy()
        self.preceding_nodes_copy = self.preceding_nodes.copy()

    def restore_node_sets(self):
        self.following_nodes = self.following_nodes_copy
        self.preceding_nodes = self.preceding_nodes_copy


def connect_node(graph, initial_node_value, following_node_value):
    initial_node = graph.all_nodes.setdefault(initial_node_value)
    if initial_node is None:
        initial_node = Node(initial_node_value)
        graph.all_nodes[initial_node_value] = initial_node
        graph.currently_accessible_nodes[initial_node_value] = initial_node

    following_node = graph.all_nodes.setdefault(following_node_value)
    if following_node is None:
        following_node = Node(following_node_value)
        graph.all_nodes[following_node_value] = following_node
    try:
        del graph.currently_accessible_nodes[following_node.value]
    except KeyError:
        pass

    initial_node.following_nodes.add(following_node)
    following_node.preceding_nodes.add(initial_node)


def build_graph_from_file(file):
    graph = Graph()
    for line in file:
        line_split_list = line.strip().split()
        initial_step = line_split_list[1]
        following_step = line_split_list[7]
        connect_node(graph, initial_step, following_step)
    return graph


if __name__ == "__main__":
    with open("07-TheSumOfItsParts-Input.txt") as input_file:
        step_graph = build_graph_from_file(input_file)
        input_file.seek(0)

        ordered_steps = step_graph.get_all_nodes_in_order()
        print(ordered_steps)

        step_graph = build_graph_from_file(input_file)
        time_spent = step_graph.work_on_nodes()
        print(time_spent)
