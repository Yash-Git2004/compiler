import { BrowserRouter, Routes, Route } from "react-router-dom";
import CodeBox from "./components/CodeBox";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CodeBox />} />
      </Routes>
    </BrowserRouter>
  );
}
