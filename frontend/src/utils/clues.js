export function getRowClues(grid) {
  return grid.map(row => {
    const clues = [];
    let count = 0;

    row.forEach(cell => {
      if (cell === 1) {
        count++;
      } else if (count > 0) {
        clues.push(count);
        count = 0;
      }
    });

    if (count > 0) clues.push(count);

    return clues.length > 0 ? clues : [0];
  });
}

export function getColumnClues(grid) {
  const size = grid.length;
  const clues = [];

  for (let col = 0; col < size; col++) {
    let count = 0;
    const colClues = [];

    for (let row = 0; row < size; row++) {
      if (grid[row][col] === 1) {
        count++;
      } else if (count > 0) {
        colClues.push(count);
        count = 0;
      }
    }

    if (count > 0) colClues.push(count);

    clues.push(colClues.length > 0 ? colClues : [0]);
  }

  return clues;
}
