import random
import tkinter as tk
from tkinter import Scale

class SortVisual:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Visualiser")

        self.canvas = tk.Canvas(self.root, width=500, height=400, bg='white')
        self.canvas.pack()

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.sort_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Sort Algorithm", menu=self.sort_menu)
        self.sort_menu.add_command(label="Bubble Sort", command=self.set_bubble_sort)
        self.sort_menu.add_command(label="Insertion Sort", command=self.set_insertion_sort)
        self.sort_menu.add_command(label="Merge Sort", command=self.set_merge_sort)
        self.sort_menu.add_command(label="Quick Sort", command=self.set_quick_sort)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_sort)
        self.start_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_sort)
        self.stop_button.pack(side=tk.LEFT)

        self.next_step_button = tk.Button(self.root, text="Next Step", command=self.next_step)
        self.next_step_button.pack(side=tk.LEFT)

        self.shuffle_button = tk.Button(self.root, text="Shuffle", command=self.shuffle_array)
        self.shuffle_button.pack(side=tk.LEFT)

        self.speed_slider = Scale(self.root, from_=1, to=1000, orient=tk.HORIZONTAL, label="Speed (ms)")
        self.speed_slider.pack(side=tk.LEFT)
        self.speed_slider.set(500)

        self.count_slider = Scale(self.root, from_=5, to=100, orient=tk.HORIZONTAL, label="Number of Elements")
        self.count_slider.pack(side=tk.LEFT)
        self.count_slider.set(30)
        self.count_slider.bind("<ButtonRelease-1>", self.update_array_size)

        self.data = []
        self.sorting = False
        self.step_mode = False
        self.sort_function = None
        self.sort_generator = None

        self.update_array_size()

    def render(self):
        self.canvas.delete("all")

        canvas_width = 500
        canvas_height = 400
        bar_width = canvas_width // len(self.data)

        for i, value in enumerate(self.data):
            x0 = i * bar_width
            y0 = canvas_height
            x1 = (i + 1) * bar_width
            y1 = canvas_height - (canvas_height * value / 110)

            self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue")
            self.canvas.create_text(x0 + bar_width / 2, y1 - 10, text=str(value), fill="black")

    def set_bubble_sort(self):
        self.sort_function = self.bubble_sort

    def set_insertion_sort(self):
        self.sort_function = self.insertion_sort

    def set_merge_sort(self):
        self.sort_function = self.merge_sort

    def set_quick_sort(self):
        self.sort_function = self.quick_sort

    def start_sort(self):
        if self.sort_function:
            self.sorting = True
            self.step_mode = False
            self.sort_generator = self.sort_function()
            self.run_sort()

    def stop_sort(self):
        self.sorting = False

    def next_step(self):
        if self.sort_function:
            self.sorting = False
            self.step_mode = True
            self.sort_generator = self.sort_function()
            self.run_sort()

    def shuffle_array(self):
        random.shuffle(self.data)
        self.render()

    def update_array_size(self, event=None):
        num_elements = self.count_slider.get()
        self.data = [random.randint(1, 100) for _ in range(num_elements)]
        self.render()

    def run_sort(self):
        if self.sorting or self.step_mode:
            try:
                next(self.sort_generator)
                self.render()
                self.root.update()
                if self.sorting:
                    speed = self.speed_slider.get()
                    self.root.after(speed, self.run_sort)
            except StopIteration:
                self.sorting = False
                self.step_mode = False

    def bubble_sort(self):
        data = self.data
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    yield

    def insertion_sort(self):
        data = self.data
        for step in range(1, len(data)):
            key = data[step]
            j = step - 1

            while j >= 0 and key < data[j]:
                data[j+1] = data[j]
                j = j - 1

            data[j+1] = key
            yield data

    def merge_sort(self):

        def merge_sort_rec(arr, start, end):
            if end - start > 1:
                middle = (start + end) // 2

                yield from merge_sort_rec(arr, start, middle)
                yield from merge_sort_rec(arr, middle, end)
                left = arr[start:middle]
                right = arr[middle:end]

                a = 0
                b = 0
                c = start

                while a < len(left) and b < len(right):
                    if left[a] < right[b]:
                        arr[c] = left[a]
                        a += 1
                    else:
                        arr[c] = right[b]
                        b += 1
                    c += 1

                while a < len(left):
                    arr[c] = left[a]
                    a += 1
                    c += 1

                while b < len(right):
                    arr[c] = right[b]
                    b += 1
                    c += 1

                yield arr

        yield from merge_sort_rec(self.data, 0, len(self.data))

    def quick_sort(self):
        def quick_sort_rec(array, low, high):
            def partition(array, low, high):
                pivot = array[high]
                i = low - 1

                for j in range(low, high):
                    if array[j] <= pivot:
                        i = i + 1
                        (array[i], array[j]) = (array[j], array[i])

                (array[i + 1], array[high]) = (array[high], array[i + 1])

                return i + 1

            if low < high:
                pi = partition(array, low, high)
                yield array
                yield from quick_sort_rec(array, low, pi - 1)
                yield from quick_sort_rec(array, pi + 1, high)

        yield from quick_sort_rec(self.data, 0, len(self.data) - 1)


if __name__ == "__main__":
    root = tk.Tk()
    app = SortVisual(root)

    root.mainloop()
