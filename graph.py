from collections import defaultdict


class Graph():
    def __init__(self):
        self.adjacency = defaultdict(set)


    def add_node(self, node):
        self.adjacency[node]


    def connections(self, node1, node2):
        self.adjacency[node1].add(node2)


    def graph_connection(self):
        return self.adjacency


