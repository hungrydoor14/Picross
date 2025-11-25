import { useSearchParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import PuzzleBoard from "../components/PuzzleBoard";

import { getRowClues, getColumnClues } from "../utils/clues";

import easyPuzzles from "../../../backend/levels/grids_10.json";
import mediumPuzzles from "../../../backend/levels/grids_15.json";
import hardPuzzles from "../../../backend/levels/grids_20.json";
import extremePuzzles from "../../../backend/levels/grids_30.json";

function makeRandomGrid(n) {
    const grid = [];
    for (let i = 0; i < n; i++) {
        const row = [];
        for (let j = 0; j < n; j++) {
            row.push(Math.random() < 0.5 ? 0 : 1);
        }
        grid.push(row);
    }
    return grid;
}

export default function Play() {
    const [won, setWon] = useState(false);
    const [puzzle, setPuzzle] = useState(null);

    const [params] = useSearchParams();
    const navigate = useNavigate();

    const type = params.get("type") || "random";
    const difficulty = params.get("difficulty") || "easy";

    const puzzleLists = {
        easy: easyPuzzles,
        medium: mediumPuzzles,
        hard: hardPuzzles,
        extreme: extremePuzzles,
    };

    // generate puzzle ONLY when type/difficulty changes
    useEffect(() => {
        let chosen = null;

        if (type === "random") {
            const n = puzzleLists[difficulty][0].grid.length;
            chosen = {
                id: Math.random(), // unique key
                grid: makeRandomGrid(n)
            };
        } else {
            const list = puzzleLists[difficulty];
            chosen = list[Math.floor(Math.random() * list.length)];
        }

        setPuzzle(chosen);
        setWon(false);   // reset win state for next puzzle
    }, [type, difficulty]);

    // puzzle not loaded yet → show nothing or loader
    if (!puzzle) return <div>Loading…</div>;

    const rowClues = getRowClues(puzzle.grid);
    const colClues = getColumnClues(puzzle.grid);

    return (
        <div className="play-container">
            <button onClick={() => navigate("/")}>← Back</button>

            <h2>
                {type === "random"
                    ? "Random Puzzle"
                    : `Premade Puzzle ID: ${puzzle.id}`}
            </h2>

            <PuzzleBoard
                key={puzzle.id} // forces fresh Board
                size={puzzle.grid.length}
                solution={puzzle.grid}
                rowClues={rowClues}
                colClues={colClues}
                onWin={() => setWon(true)}
            />

            {won && (
                <div className="win-banner">
                    🎉 YOU WIN!!! 🎉
                </div>
            )}
        </div>
    );
}
