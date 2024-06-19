import tkinter as tk
from tkinter import Scale
import heapq


class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    def __hash__(self):
        return hash(self.position)


class AStarVisual:
    def __init__(self, root):
        self.root = root
        self.root.title("A* Algorithm Visualiser")

        self.canvas = tk.Canvas(self.root, width=500, height=400, bg='white')
        self.canvas.pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start_search)
        self.start_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_search)
        self.stop_button.pack(side=tk.LEFT)

        self.next_step_button = tk.Button(self.root, text="Next Step", command=self.next_step)
        self.next_step_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_search)
        self.reset_button.pack(side=tk.LEFT)

        self.speed_slider = Scale(self.root, from_=1, to=1000, orient=tk.HORIZONTAL, label="Speed (ms)")
        self.speed_slider.pack(side=tk.LEFT)
        self.speed_slider.set(500)

        self.searching = False
        self.step_mode = False
        self.search_function = None
        self.search_generator = None

        self.initialize_search()

    def render(self, path):
        self.canvas.delete("all")
        canvas_width = 500
        canvas_height = 400
        bar_width = canvas_width // len(self.maze[0])
        bar_height = canvas_height // len(self.maze)

        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                color = 'black' if self.maze[i][j] == 1 else 'white'
                x0 = j * bar_width
                y0 = i * bar_height
                x1 = (j + 1) * bar_width
                y1 = (i + 1) * bar_height
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

        for position in path:
            x0 = position[1] * bar_width
            y0 = position[0] * bar_height
            x1 = (position[1] + 1) * bar_width
            y1 = (position[0] + 1) * bar_height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill='blue')

    def initialize_search(self):
        self.maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.start = (0, 0)
        self.end = (7, 6)
        self.path = []
        self.render(self.path)

    def start_search(self):
        self.searching = True
        self.step_mode = False
        self.search_generator = self.astar(self.maze, self.start, self.end)
        self.run_search()

    def stop_search(self):
        self.searching = False

    def next_step(self):
        if not self.step_mode:
            self.searching = False
            self.step_mode = True
            self.search_generator = self.astar(self.maze, self.start, self.end)
        self.run_search()

    def reset_search(self):
        self.searching = False
        self.step_mode = False
        self.initialize_search()

    def run_search(self):
        if self.searching or self.step_mode:
            try:
                self.path = next(self.search_generator)
                self.render(self.path)
                if self.searching:
                    speed = self.speed_slider.get()
                    self.root.after(speed, self.run_search)
            except StopIteration:
                self.searching = False

    def astar(self, maze, start, end):
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        open_list = []
        heapq.heappush(open_list, (start_node.f, start_node))

        while open_list:
            current_node = heapq.heappop(open_list)[1]
            closed_list = set()

            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                yield path[::-1]  # Gibt den gefundenen Pfad zurück
                return  # Beendet den Generator

            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                        len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                    continue

                if maze[node_position[0]][node_position[1]] != 0:
                    continue

                new_node = Node(current_node, node_position)

                children.append(new_node)

            for child in children:
                if child in closed_list:
                    continue

                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                            (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                if add_to_open(open_list, child):
                    heapq.heappush(open_list, (child.f, child))
                    yield get_path(child)  # Gibt den aktuellen Pfad bis zu diesem Kind zurück


def add_to_open(open_list, child):
    for node in open_list:
        if child == node[1] and child.g > node[1].g:
            return False
    return True


def get_path(node):
    path = []
    current = node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]


if __name__ == '__main__':
    root = tk.Tk()
    visualiser = AStarVisual(root)
    root.mainloop()
