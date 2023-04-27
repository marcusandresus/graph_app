class Node:
    RADIUS = 20

    def __init__(self, x, y, label=None):
        self.x = x
        self.y = y
        self.label = label if label is not None else f"Node {id(self)}"
        self.edges = []

    def move(self, x, y):
        self.x = x
        self.y = y

    def add_edge(self, edge):
        self.edges.append(edge)

    def remove_edge(self, edge):
        self.edges.remove(edge)
