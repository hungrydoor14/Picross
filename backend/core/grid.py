import random
import json, os

class PicrossGrid:
    """
    This class is meant to create the functionality for the picross grid.

    Difficulty thought process:
        Easy: either 7x7 or 10x10
        Medium: 15x15
        Hard: 20x20
        Expert(?): 30x30

    """

    def make_grid(n):
        """
        returns a n*n grid of a randomly generated puzzle of 1s (black) and 0s (empty)
        """
        grid = [[0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for j in range(n):
                grid[i][j] = random.randint(0, 1)

        return grid
    
    def make_premade_grid(id, n):
        """
        Loads a premade grid by ID from grids_{n}.json
        and returns it as a 2D array of 1s/0s.

        grid_id: int
        n: grid size (5, 10, 15, 20, etc.)
        """
        # get absolute project root (folder that contains backend/)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
        # backend/levels/
        levels_dir = os.path.join(base_dir, "levels")
        
        # backend/levels/grids_10.json
        file_path = os.path.join(levels_dir, f"grids_{n}.json")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No level file found: {file_path}")
        
        # load the JSON list
        with open(file_path, "r") as f:
            data = json.load(f)

        # find the grid with matching ID
        for entry in data:
            if entry["id"] == id:
                return entry["grid"]

        raise ValueError(f"Grid with id {id} not found for size {n}.")
    
    def visualize_key_grid(grid, filled="■ ", empty=". "):
        """
        Given an array grid and the optional visualization characters, it will show you on the
        terminal how it would look
        """
        n = len(grid)

        for i in range(n):
            row_str = ""
            for j in range(n):
                if grid[i][j] == 1:
                    row_str += filled
                else:
                    row_str += empty
            print(row_str)