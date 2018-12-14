class Tree:
    def __init__(self, root):
        self.root = root

    def get_sum_of_all_nodes_metadata(self):
        return self.root.get_sum_of_own_metadata() + self.root.sum_of_child_metadata


class Node:
    def __init__(self, parent_node=None, child_node_amount=None, metadata_amount=None):
        self.parent_node = parent_node
        self.child_node_amount = child_node_amount
        self.metadata_amount = metadata_amount
        self.child_nodes = []
        self.metadata = []
        self.sum_of_child_metadata = 0
        self.value = 0

    def get_sum_of_own_metadata(self):
        return sum(self.metadata)

    def assign_value(self):
        if not self.child_nodes:
            self.value = self.get_sum_of_own_metadata()
            return
        for data_index in self.metadata:
            try:
                metadata_child_node = self.child_nodes[data_index - 1]
                self.value += metadata_child_node.value
            except IndexError:
                pass


def build_tree_from_data(node_data):
    current_node = None
    tree = None

    for data in node_data:
        if current_node is None:
            current_node = Node(child_node_amount=data)
            tree = Tree(current_node)
        elif current_node.metadata_amount is None:
            current_node.metadata_amount = data
        elif len(current_node.child_nodes) < current_node.child_node_amount:
            new_node = Node(current_node, child_node_amount=data)
            current_node.child_nodes.append(new_node)
            current_node = new_node
        elif len(current_node.metadata) < current_node.metadata_amount:
            current_node.metadata.append(data)
            if len(current_node.metadata) == current_node.metadata_amount:
                current_node.assign_value()

                try:
                    current_node.parent_node.sum_of_child_metadata += current_node.get_sum_of_own_metadata()
                    current_node.parent_node.sum_of_child_metadata += current_node.sum_of_child_metadata
                    current_node = current_node.parent_node

                # If the current node is the root node, its parent node is None, which has no sum_of_child_metadata
                # But we do not need to find that sum for the parent of the root node (since it does not exist), and
                # do not need to update the current node to this non-existent value, so we safely except and pass
                except AttributeError:
                    pass
    return tree


def format_data_list(data_string):
    data_list = data_string.split()
    for num, data in enumerate(data_list):
        data_list[num] = int(data.strip())
    return data_list


def main():
    with open("08-MemoryManeuver-Input.txt") as input_file:
        node_data_string = input_file.readlines()[0]

    node_data_list = format_data_list(node_data_string)
    node_tree = build_tree_from_data(node_data_list)

    metadata_sum = node_tree.get_sum_of_all_nodes_metadata()
    print(metadata_sum)
    root_value = node_tree.root.value
    print(root_value)


if __name__ == "__main__":
    main()