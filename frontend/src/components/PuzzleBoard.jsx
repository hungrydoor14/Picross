import { useState, useRef, useEffect } from "react";
import "./PuzzleBoard.css";

export default function PuzzleBoard({ size, solution, rowClues, colClues, onWin }) {
  const [grid, setGrid] = useState(
    Array(size).fill(null).map(() => Array(size).fill(0))
  );

  useEffect(() => {
    setGrid(Array(size).fill(null).map(() => Array(size).fill(0)));
  }, [size]);

  useEffect(() => {
    const solved = grid.every((row, r) =>
      row.every((cell, c) => {
        const target = solution[r][c];

        // Filled cell must match exactly:
        if (target === 1) return cell === 1;

        // Empty cell in solution: allow either empty or X
        if (target === 0) return cell === 0 || cell === 2;

        return false;
      })
);

    if (solved) onWin();
  }, [grid, solution, onWin]);

  const isDrawing = useRef(false);
  const isRightDragging = useRef(false);
  const drawValue = useRef(1);
  const eraseType = useRef(null);
  const rightClickMode = useRef(null);

  // LEFT CLICK (black mode)
  const handleMouseDown = (row, col) => {
    // if clicking X, ignore drawing
    if (grid[row][col] === 2) return;

    // determine if drawing or erasing
    if (grid[row][col] === 1) {
      drawValue.current = 0;   // erase
      eraseType.current = 1;   // erase black
    } else {
      drawValue.current = 1;   // draw black
      eraseType.current = null;
    }

    isDrawing.current = true;
    toggleCell(row, col);
  };

  // RIGHT CLICK (X mode)
  const handleRightClick = (row, col, e) => {
    e.preventDefault();
    isRightDragging.current = true;

    const cell = grid[row][col];

    if (cell === 2) {
      // clicking an X → erase mode
      rightClickMode.current = "erase";
    } else if (cell === 0) {
      // clicking white → add mode
      rightClickMode.current = "add";
    } else {
      // clicking black → do nothing
      return;
    }

    toggleX(row, col);
  };


  // This handles black draw/erase with rules
  const toggleCell = (row, col) => {
    setGrid(prev => {
      const newGrid = prev.map(r => [...r]);
      const cell = newGrid[row][col];

      // prevent drawing over an X
      if (drawValue.current === 1 && cell === 2) return prev;

      // erase only the type you started erasing
      if (drawValue.current === 0) {
        if (eraseType.current === 1 && cell !== 1) return prev;
        if (eraseType.current === 2 && cell !== 2) return prev;
      }

      newGrid[row][col] = drawValue.current;
      return newGrid;
    });
  };

  // This handles X-drag mode
  const toggleX = (row, col) => {
    setGrid(prev => {
      const newGrid = prev.map(r => [...r]);

      const cell = newGrid[row][col];

      if (rightClickMode.current === "add") {
        // Only add X to white cells
        if (cell === 0) newGrid[row][col] = 2;
      }

      if (rightClickMode.current === "erase") {
        // Only erase X cells
        if (cell === 2) newGrid[row][col] = 0;
      }

      return newGrid;
    });
  };


  // DRAGGING
  const handleMouseEnter = (row, col) => {
    if (isDrawing.current) toggleCell(row, col);
    if (isRightDragging.current) toggleX(row, col);
  };

  const handleMouseUp = () => {
    isDrawing.current = false;
    isRightDragging.current = false;
    eraseType.current = null;
  };

  return (
    <div className="picross-container" style={{ "--size": size }}>

      <div className="corner"></div>

      <div className="column-clues">
        {colClues.map((colGroup, colIndex) => (
          <div key={colIndex} className="clue-col">
            {colGroup.map((n, i) => (
              <div key={i} className="clue-number">{n}</div>
            ))}
          </div>
        ))}
      </div>

      <div className="row-clues">
        {rowClues.map((rowGroup, rowIndex) => (
          <div key={rowIndex} className="clue-row">
            {rowGroup.map((n, i) => (
              <div key={i} className="clue-number">{n}</div>
            ))}
          </div>
        ))}
      </div>

      <div
        className="board"
        style={{
          gridTemplateColumns: `repeat(${size}, 1fr)`,
          gridTemplateRows: `repeat(${size}, 1fr)`
        }}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onContextMenu={(e) => e.preventDefault()}
      >
        {grid.map((row, r) =>
          row.map((cell, c) => (
            <div
              key={`${r}-${c}`}
              className={`cell 
                ${cell === 1 ? "filled" : ""} 
                ${cell === 2 ? "x-mark" : ""}
              `}
              draggable={false}
              onDragStart={(e) => e.preventDefault()}

              onMouseDown={(e) => {
                if (e.button === 0) handleMouseDown(r, c);
              }}
              onContextMenu={(e) => handleRightClick(r, c, e)}
              onMouseEnter={() => handleMouseEnter(r, c)}
            />
          ))
        )}
      </div>
    </div>
  );
}
