import tkinter as tk


class PopupMenu:
    """A class for the popup menu that appears when right-clicking on nodes or canvas."""

    def __init__(
        self,
        gr_app,  # graphapp object
        master,
        canvas,
        node_menu_callback,
        canvas_menu_callback,
        edge_menu_callback,
    ):
        """Initialize the popup menu."""
        self.gr_app = gr_app
        self.master = master
        self.canvas = canvas
        self.node_menu_callback = node_menu_callback
        self.canvas_menu_callback = canvas_menu_callback
        self.edge_menu_callback = edge_menu_callback
        self.last_action = None
        self.selected_node = None

        self.popup_menu = tk.Menu(self.master, tearoff=0)
        self.popup_menu.add_command(label="Add node", command=self._add_node)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Add edge", command=self._add_edge)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Remove node", command=self._remove_node)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Remove edge", command=self._remove_edge)

        self.node_menu = tk.Menu(self.master, tearoff=0)
        self.node_menu.add_command(label="Add edge", command=self._add_edge)
        self.node_menu.add_command(label="Remove node", command=self._remove_node)
        # self.node_menu.add_command(label="Remove edge", command=self._remove_edge, )

    def _add_node(self):
        """Callback for adding a node to the graph."""
        x, y = self.canvas.canvasx(self.canvas.winfo_pointerx()), self.canvas.canvasy(
            self.canvas.winfo_pointery()
        )
        self.node_menu_callback(x, y)
        self.last_action = "Add node"
        self.selected_node = None

    def _add_edge(self):
        """Callback for adding an edge to the graph."""
        print("_add_edge")
        self.canvas.unbind("<Button-1>")
        self.canvas.bind("<Button-1>", self._add_edge_first_node)
        self.last_action = "Add edge"
        self.selected_node = None

    def _add_edge_first_node(self, event):
        """Callback for selecting the first node for adding an edge."""
        print("_add_edge_first_node")
        self.canvas.unbind("<Button-1>")
        # node1 = self.canvas.find_withtag("current")[0]
        node1 = self.gr_app.get_node_at_pos(event.x, event.y)
        self.canvas.bind("<Button-1>", self._add_edge_second_node)
        self.canvas.itemconfig(node1, outline="red")
        self.canvas.tag_raise(node1)
        self.selected_node = node1

    def _add_edge_second_node(self, event):
        """Callback for selecting the second node and completing the edge addition."""
        print("_add_edge_second_node")
        self.canvas.unbind("<Button-1>")
        node1 = self.selected_node
        # node2 = self.canvas.find_closest(event.x, event.y)[0]
        node2 = self.gr_app.get_node_at_pos(event.x, event.y)
        print("node2: ", str(node2))
        # if node1 != node2 and node1 in self.canvas.gettags(node2):
        if node1 != node2:
            self.edge_menu_callback(node1, node2)
            self.last_action = "Add edge"
            self.selected_node = None
        else:
            self.last_action = None
            self.selected_node = None
        self.canvas.itemconfig(node1, outline="black")

    def _remove_node(self):
        """Callback for removing a node from the graph."""
        node = self.canvas.find_withtag("current")[0]
        self.node_menu_callback(node)
        self.last_action = "Remove node"
        self.selected_node = None

    def _remove_edge(self):
        """Callback for removing an edge from the graph."""
        self.canvas.unbind("<Button-1>")
        self.canvas.bind("<Button-1>", self._remove_edge_first_node)
        self.last_action = "Remove edge"
        self.selected_node = None

    def _remove_edge_first_node(self, event):
        """Callback for selecting the first node for removing an edge."""
        self.canvas.unbind("<Button-1>")
        node1 = self.canvas.find_withtag("current")[0]
        self.canvas.bind("<Button-1>", self._remove_edge_second_node)
        self.canvas.itemconfig(node1, outline="red")
        self.canvas.tag_raise(node1)

    def _remove_edge_second_node(self, event):
        """Callback for selecting the second node and completing the edge removal."""
        self.canvas.unbind("<Button-1>")
        node1 = self.selected_node
        node2 = self.canvas.find_closest(event.x, event.y)[0]
        if node1 != node2 and node1 in self.canvas.gettags(node2):
            self.edge_menu_callback(node1, node2)
        self.canvas.itemconfig(node1, outline="black")
        self.last_action = "remove_edge"
        self.selected_node = None

    def show_canvas_menu(self, event_x_root, event_y_root):
        """Show the canvas popup menu."""
        self.popup_menu.post(event_x_root, event_y_root)
        print("show_canvas_menu")

    def show_node_menu(self, event_x_root, event_y_root):
        """Show the node popup menu."""
        print("show_node_menu")
        self.canvas.focus_set()
        self.node_menu.post(event_x_root, event_y_root)
        # self.popup_menu.entryconfig("Add edge", state=tk.DISABLED)
        # tags = self.canvas.gettags("current")
        # print(f"tags: {tags}")
        # if "node" in tags:
        #     self.popup_menu.entryconfig("Remove node", state=tk.NORMAL)
        #     self.popup_menu.post(event_x_root, event_y_root)
        # else:
        #     self.popup_menu.post(event_x_root, event_y_root)
        self.node_menu.bind("<Unmap>", self.clear_last_action)

    def clear_last_action(self):
        print("cleared last action")
        self.last_action = None
