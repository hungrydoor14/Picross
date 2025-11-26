import { useState } from "react";
import { useNavigate } from "react-router-dom";
import PuzzleBoard from "../components/PuzzleBoard"; // REMOVE IF YOU WANT NO BOARD ON MENU
import "./Menu.css";

export default function Menu() {
  const [difficulty, setDifficulty] = useState("easy");
  const navigate = useNavigate();

  const sizeMap = {
    easy: 10,
    medium: 15,
    hard: 20,
    extreme: 30,
  };

const goRandom = () => {
  navigate(`/play?type=random&difficulty=${difficulty}`);
};

const goPremade = () => {
  navigate(`/play?type=premade&difficulty=${difficulty}`);
};

  return (
    <div className="menu-container">
      <h1 className="title">Picross</h1>

      <div className="difficulty-section">
        <label>Difficulty: </label>
        <select
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
        >
          <option value="easy">Easy (10x10)</option>
          <option value="medium">Medium (15x15)</option>
          <option value="hard">Hard (20x20)</option>
          <option value="extreme">Extreme (30x30)</option>
        </select>
      </div>
        <div></div>
        <div className="menu-buttons">
                <button className="menu-btn" onClick={goRandom}>
                    Random Puzzle
                </button>

                <button className="menu-btn" onClick={goPremade}>
                    Premade Puzzle
                </button>
        </div>
        <div classname="instructions">
          <h2>How to play:</h2>
          Left click to fill a cell, right click to mark a cell as empty. <br/>
          Complete the grid according to the numbers on the top and left sides.
        </div>
    </div>
  );
}
