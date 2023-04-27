from gui.edge import Edge


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.temp_edge = None

    def add_node(self, node):
        self.nodes.append(node)

    def remove_node(self, node):
        self.nodes.remove(node)
        edges_to_remove = [edge for edge in self.edges if node in edge]
        for edge in edges_to_remove:
            self.remove_edge(edge)

    def add_edge_temp(self, node):
        if self.temp_edge is None:
            self.temp_edge = Edge(node, None)
        else:
            self.temp_edge.node2 = node
            self.add_edge(self.temp_edge)
            self.temp_edge = None

    def add_edge(self, edge):
        if edge not in self.edges:
            node1, node2 = edge.node1, edge.node2
            node1.add_edge(edge)
            node2.add_edge(edge)
            self.edges.append(edge)

    def remove_edge(self, edge):
        if edge in self.edges:
            node1, node2 = edge.node1, edge.node2
            node1.remove_edge(edge)
            node2.remove_edge(edge)
            self.edges.remove(edge)

    def get_adjacent_nodes(self, node):
        adjacent_nodes = set()
        for edge in self.edges:
            if node in edge:
                adjacent_nodes.update(edge)
        adjacent_nodes.remove(node)
        return list(adjacent_nodes)

    def update_edges(self):
        for edge in self.edges:
            edge.update_position()

    def has_edge(self, node1, node2):
        for edge in self.edges:
            if (edge.node1 == node1 and edge.node2 == node2) or (
                edge.node1 == node2 and edge.node2 == node1
            ):
                return True
        return False
