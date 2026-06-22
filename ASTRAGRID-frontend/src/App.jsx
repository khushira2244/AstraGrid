import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import AstraGridLanding from "./pages/AstraGridLanding";
import AstraGridDemo from "./pages/AstraGridDemo";
import AstraGridArchitecture from "./pages/AstraGridArchitecture";
import AstraGridLearnMore from "./pages/AstraGridLearnMore.jsx";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AstraGridLanding />} />
        <Route path="/demo" element={<AstraGridDemo />} />
        <Route path="/architecture" element={<AstraGridArchitecture />} />
        <Route path="/learnmore" element={<AstraGridLearnMore />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
