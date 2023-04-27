import tkinter as tk
from tkinter import filedialog, messagebox
from .node import Node
from .edge import Edge
from .popup_menu import PopupMenu
from graph.graph import Graph


class GraphApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Graph Editor")
        self.root.geometry("800x600")
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill="both", expand=True)
        self.graph = Graph()
        self.popup_menu = PopupMenu(
            self, self.root, self.canvas, self.graph, self.update_canvas, None
        )
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<B1-Motion>", self.on_canvas_motion)
        self.canvas.bind("<Button-3>", self.on_right_click)

    def run(self):
        self.root.mainloop()

    def on_right_click(self, event):
        node = self.get_node_at_pos(event.x, event.y)
        if node is not None:
            print(f"node {node.label} selected")
            self.popup_menu.show_node_menu(event.x_root, event.y_root)
        else:
            print("canvas selected, show canvas menu")
            self.popup_menu.show_canvas_menu(event.x_root, event.y_root)
            if self.popup_menu.last_selection == "Add edge":
                self.graph.add_edge_temp(self.get_node_at_pos(event.x, event.y))
            else:
                self.graph.add_edge_temp(None)

    def on_canvas_click(self, event):
        print(f"canvas_click {event.x}, {event.y}")
        node = self.get_node_at_pos(event.x, event.y)
        if node is None:
            node = Node(event.x, event.y)
            print(f"... creating node {node.label}")
            self.graph.add_node(node)
            self.update_canvas()
            self.popup_menu.last_selection = None  # reset last selection
        else:
            print("... there is a node")
            self.popup_menu.last_selection = node  # set last selection to clicked node

    def on_canvas_release(self, event):
        self.graph.update_edges()

    def on_canvas_motion(self, event):
        node = self.get_node_at_pos(event.x, event.y)
        if node is not None:
            node.move(event.x, event.y)
            self.graph.update_edges()
            self.update_canvas()

    # def on_menu_dismissed(self):
    #     print("menu dismissed (check when an option is selected)")
    #     self.popup_menu.last_selection = None

    def update_canvas(self):
        self.canvas.delete("all")
        for edge in self.graph.edges:
            self.canvas.create_line(
                edge.node1.x, edge.node1.y, edge.node2.x, edge.node2.y
            )
        for node in self.graph.nodes:
            self.canvas.create_oval(
                node.x - Node.RADIUS,
                node.y - Node.RADIUS,
                node.x + Node.RADIUS,
                node.y + Node.RADIUS,
                fill="white",
            )
            self.canvas.create_text(node.x, node.y, text=node.label)

    def get_node_at_pos(self, x, y):
        for node in self.graph.nodes:
            if (node.x - x) ** 2 + (node.y - y) ** 2 <= Node.RADIUS**2:
                return node
        return None

    def create_edge(self, node1, node2):
        if node1 != node2 and not self.graph.has_edge(node1, node2):
            edge = Edge(node1, node2)
            self.graph.add_edge(edge)
            self.update_canvas()
