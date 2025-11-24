def grids_match(grid1, grid2):
    """
    Returns True if the two grids match exactly.
    Grids must be 2D lists of equal dimensions.
    """
    if len(grid1) != len(grid2):
        return False
    
    for row_a, row_b in zip(grid1, grid2):
        if row_a != row_b:
            return False
    
    return True

def grids_match_partial(player, solution):
    """
    Returns True if player grid has only correct squares so far.
    Does NOT require the puzzle to be finished.
    """
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            if player[i][j] == 1 and solution[i][j] != 1:
                return False
    return True

