class BaseGraph(object):
    def __init__(self, graph_dict):
        self.adjacency_list = graph_dict

    def add_node(self, node):
        if node in self.adjacency_list:
            raise Exception("Node already exists")
        self.adjacency_list[node] = set()

    def add_edge(self, node_1, node_2):
        self.adjacency_list[node_1].add(node_2)
        self.adjacency_list[node_2].add(node_2)

    def get_adjacent_nodes(self, node):
        return self.adjacency_list[node]