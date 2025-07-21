import { BrowserRouter, Routes, Route } from "react-router-dom";
import SignupPage from "./components/SignUpPage/SignUpPage";
import LoginPage from "./components/LoginPage/LoginPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SignupPage />} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
