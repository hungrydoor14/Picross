import { BrowserRouter, Routes, Route } from "react-router-dom";
import Menu from "./screens/Menu";
import Play from "./screens/Play";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Menu />} />
        <Route path="/play" element={<Play />} />
      </Routes>
    </BrowserRouter>
  );
}
