import random

class PicrossGrid:
    """
    This class is meant to create the functionality for the picross grid.
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
    
    def visualize_key_grid(grid, filled="■ ", empty=". "):
        n = len(grid)

        for i in range(n):
            row_str = ""
            for j in range(n):
                if grid[i][j] == 1:
                    row_str += filled
                else:
                    row_str += empty
            print(row_str)