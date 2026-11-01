from collections import defaultdict


class Graph():
    def __init__(self):
        self.adjacency = defaultdict(set)


    def add_node(self, node):
        self.adjacency[node]


    def connections(self, from_node, to_node):
        self.adjacency[from_node].add(to_node)
        self.adjacency[to_node].add(from_node)


    def graph_connection(self):
        return self.adjacency


