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

        # Enable keep_square AFTER initial render
        self.root.after(50, lambda: self.root.bind("<Configure>", self.keep_square))

        # GRID FRAME
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(fill="both", expand=True)

        # Canvas inside the frame
        self.canvas = tk.Canvas(self.grid_frame, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Canvas resizing handler
        self.canvas.bind("<Configure>", self.on_resize)

        # BUTTON BAR 
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Export Grid", command=self.export_grid).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Clear All", command=self.clear_grid).pack(side="left", padx=5)

        # Click to toggle cells
        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_grid()
        self.root.mainloop()

    def draw_grid(self):
        self.canvas.delete("all")

        cell = self.cell_size
        for i in range(self.n):
            for j in range(self.n):
                x1 = j * cell
                y1 = i * cell
                x2 = x1 + cell
                y2 = y1 + cell

                fill = "black" if self.grid[i][j] else "white"

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=fill, outline="gray"
                )

    def on_resize(self, event):
        """ Resize grid based on cavnas size"""
        # Determine new square side
        size = min(event.width, event.height)
        self.cell_size = size / self.n
        self.draw_grid()

    def keep_square(self, event):
        """ keep window square"""
        if event.widget is self.root:
            size = min(event.width, event.height)
            self.root.geometry(f"{size}x{size+60}")  
            # +60 = button height

    def on_click(self, event):
        """ mouse click toggles action """
        j = int(event.x // self.cell_size)
        i = int(event.y // self.cell_size)

        if 0 <= i < self.n and 0 <= j < self.n:
            self.grid[i][j] ^= 1
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
