import time
import tkinter as tk
from AStar import astar_generator as astar
from Dijkstra import dijkstra_generator as dijkstra
from Bfs import bfs_generator as bfs

class PathFinder:
    def __init__(self, root, grid=[], start=None, end=None):
        self.root = root
        self.root.title("Pathfinding Visualiser")

        # window
        self.canvas = tk.Canvas(self.root, width=500, height=400, bg='white')
        self.canvas.pack()

        # algorithm menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.sort_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Pathfinding Algorithm", menu=self.sort_menu)
        self.sort_menu.add_command(label="A*", command=self.set_astar_finder)
        self.sort_menu.add_command(label="Dijkstra", command=self.set_dijkstra_finder)
        self.sort_menu.add_command(label="Breath First", command=self.set_bfs_finder)
        # bottom menu
        self.start_button = tk.Button(self.root, text="Start", command=self.start_algorithm)
        self.start_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_algorithm)
        self.stop_button.pack(side=tk.LEFT)

        self.next_step_button = tk.Button(self.root, text="Next Step", command=self.next_step)
        self.next_step_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_grid)
        self.reset_button.pack(side=tk.LEFT)

        self.speed_slider = tk.Scale(self.root, from_=1, to=1000, orient=tk.HORIZONTAL, label="Speed (ms)")
        self.speed_slider.pack(side=tk.LEFT)
        self.speed_slider.set(1)


        # data
        self.grid = grid
        self.path = []
        self.search = []
        self.start_point = start
        self.end_point = end
        self.algorithm = astar
        self.running = False
        self.step_mode = False
        self.current_path_generator = None
        self.current_search_generator = None

        self.initialize_grid()

    def set_dijkstra_finder(self):
        self.algorithm = dijkstra

    def set_astar_finder(self):
        self.algorithm = astar

    def set_bfs_finder(self):
        self.algorithm = bfs

    def start_algorithm(self):
        self.running = True
        self.step_mode = False
        if self.current_path_generator is None:
            self.current_path_generator, self.current_search_generator = self.algorithm(self.grid, (self.start_point[0], self.start_point[1]), (self.end_point[0], self.end_point[1]))
        self.run_algorithm()

    def stop_algorithm(self):
        self.running = False

    def next_step(self):
        self.step_mode = True
        if self.current_path_generator is None:
            self.current_path_generator, self.current_search_generator = self.algorithm(self.grid, (self.start_point[0], self.start_point[1]), (self.end_point[0], self.end_point[1]))
        try:
            self.path.append(next(self.current_path_generator))
            self.search.append(next(self.current_search_generator))
            self.render()
        except StopIteration:
            self.current_path_generator = None

    def reset_grid(self):
        self.running = False
        self.step_mode = []
        self.current_path_generator = None
        self.current_search_generator = None
        self.initialize_grid()

    def initialize_grid(self):
        self.path = []
        self.search = []
        self.render()

    def render(self):
        self.canvas.delete("all")
        canvas_width = 500
        canvas_height = 400
        width = canvas_width // len(self.grid[0])
        height = canvas_height // len(self.grid)

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                color = 'black' if self.grid[i][j] == 1 else 'white'
                x0 = j * width
                y0 = i * height
                x1 = (j + 1) * width
                y1 = (i + 1) * height
                rect_id = self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

                self.canvas.tag_bind(rect_id, '<Button-1>', lambda event, i=i, j=j: self.toggle_grid_cell(i, j))

        for position in self.search:
            x0 = position[1] * width
            y0 = position[0] * height
            x1 = (position[1] + 1) * width
            y1 = (position[0] + 1) * height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill='yellow')

        for position in self.path:
            x0 = position[1] * width
            y0 = position[0] * height
            x1 = (position[1] + 1) * width
            y1 = (position[0] + 1) * height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill='blue')

    def toggle_grid_cell(self, i, j):
        self.grid[i][j] = 1 - self.grid[i][j]
        self.render()

    def run_algorithm(self):
        if self.algorithm is not None and self.current_path_generator is not None:
            self.update_path()

    def update_path(self):
        if self.running and self.current_path_generator is not None and self.current_search_generator is not None:
            try:
                self.path.append(next(self.current_path_generator))
                self.search.append(next(self.current_search_generator))
                self.render()
                speed = self.speed_slider.get()
                self.root.after(speed, self.update_path)
            except StopIteration:
                self.current_path_generator = None


if __name__ == "__main__":
    matrix = \
        [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
        ]
    start = (0, 0)
    end = (12, 7)

    root = tk.Tk()
    app = PathFinder(root, matrix, start, end)

    root.mainloop()
