import tkinter as tk
from tkinter import simpledialog, messagebox
import json, os

class LevelMaker:
    def __init__(self, n=10):
        self.n = n
        self.grid = [[0 for _ in range(n)] for _ in range(n)]
        self.cell_size = 30

        # ROOT WINDOW
        self.root = tk.Tk()
        self.root.title("Picross Level Maker")

        # Set initial window size BEFORE square enforcement kicks in
        initial_size = max(400, self.n * 30)
        self.root.geometry(f"{initial_size}x{initial_size+60}")

        # GRID FRAME
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(fill="both", expand=True)

        # Canvas inside the frame
        self.canvas = tk.Canvas(self.grid_frame, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Keep square
        self.canvas.bind("<Configure>", self.keep_square)

        # Canvas resizing handler
        self.canvas.bind("<Configure>", self.on_resize)

        # BUTTON BAR 
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Export Grid", command=self.export_grid).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Clear All", command=self.clear_grid).pack(side="left", padx=5)

        # DRAWING 
        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.is_drawing = False
        self.already_toggled = set()
        self.draw_value = None

        self.draw_grid()
        self.root.mainloop()

    def draw_grid(self):
        self.canvas.delete("all")

        cell = self.cell_size

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()

        grid_px = cell * self.n

        # Center offsets
        offset_x = (canvas_w - grid_px) / 2
        offset_y = (canvas_h - grid_px) / 2

        for i in range(self.n):
            for j in range(self.n):
                x1 = offset_x + j * cell
                y1 = offset_y + i * cell
                x2 = x1 + cell
                y2 = y1 + cell

                fill = "black" if self.grid[i][j] else "white"

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=fill, outline="gray"
                )

    def event_to_cell(self, event):
        """Convert mouse coordinates to (row, col) respecting centered grid"""
        cell = self.cell_size

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        grid_px = cell * self.n

        offset_x = (canvas_w - grid_px) / 2
        offset_y = (canvas_h - grid_px) / 2

        # Adjust event coordinates
        x = event.x - offset_x
        y = event.y - offset_y

        # Ignore clicks outside the grid
        if x < 0 or y < 0 or x >= grid_px or y >= grid_px:
            return None, None

        j = int(x // cell)
        i = int(y // cell)
        return i, j


    def on_resize(self, event):
        """ Resize grid based on cavnas size"""
        # ignore garbage events during fullscreen transition
        if event.width <= 1 or event.height <= 1:
            return  
    
        # Determine new square side
        size = min(event.width, event.height)
        self.cell_size = size / self.n
        self.draw_grid()

    def keep_square(self, event):
        """Keep ONLY the canvas square — NOT the whole window"""
        if event.widget is self.canvas:
            size = min(event.width, event.height)
            self.canvas.config(width=size, height=size)


    def on_press(self, event):
        self.is_drawing = True
        self.already_toggled = set()

        # determine drawing mode: 1 = draw, 0 = erase
        j = int(event.x // self.cell_size)
        i = int(event.y // self.cell_size)

        if 0 <= i < self.n and 0 <= j < self.n:
            self.draw_value = 0 if self.grid[i][j] == 1 else 1

        self._apply_brush(event)


    def on_drag(self, event):
        """Toggle cells as you drag across them."""
        if self.is_drawing:
            self._apply_brush(event)

    def on_release(self, event):
        self.is_drawing = False
        self.already_toggled = set()
        self.draw_value = None

    def _apply_brush(self, event):
        i, j = self.event_to_cell(event)
        if i is None:    # click outside grid
            return

        if 0 <= i < self.n and 0 <= j < self.n:
            cell_id = (i, j)
            if cell_id not in self.already_toggled:
                self.grid[i][j] = self.draw_value 
                self.already_toggled.add(cell_id)
                self.draw_grid()


    def export_grid(self):
        base_dir = os.path.abspath(os.path.dirname(__file__))
        save_dir = os.path.join(base_dir, "levels")

        os.makedirs(save_dir, exist_ok=True)

        save_path = os.path.join(save_dir, f"grids_{self.n}.json")

        # Load existing
        if os.path.exists(save_path):
            with open(save_path, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        # Compute next ID
        next_id = data[-1]["id"] + 1 if data else 1

        # Append new data
        data.append({
            "id": next_id,
            "grid": self.grid
        })

        # MANUAL JSON FORMATTER
        # the files were darn unreadable before. Overcomplicated. Awful. Works. 
        output_lines = ["["]

        for i, entry in enumerate(data):
            output_lines.append("    {")
            output_lines.append(f"        \"id\": {entry['id']},")
            output_lines.append("        \"grid\": [")

            # rows with NO trailing comma on last one
            for r_idx, row in enumerate(entry["grid"]):
                row_str = "[" + ",".join(str(x) for x in row) + "]"
                if r_idx < len(entry["grid"]) - 1:
                    output_lines.append(f"            {row_str},")
                else:
                    output_lines.append(f"            {row_str}")

            output_lines.append("        ]")

            # comma between objects, but not after the last one
            if i < len(data) - 1:
                output_lines.append("    },")
            else:
                output_lines.append("    }")

        output_lines.append("]")

        # Write it
        with open(save_path, "w") as f:
            f.write("\n".join(output_lines))

        messagebox.showinfo("Saved!", f"Grid #{next_id} saved to:\n{save_path}")

    def clear_grid(self):
        """ clear grid if it is too bad to just manually refresh """
        self.grid = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.draw_grid()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    n = simpledialog.askinteger("Grid size", "Enter grid size:", minvalue=2, maxvalue=50)
    root.destroy()

    if n:
        LevelMaker(n)
