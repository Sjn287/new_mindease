import { BrowserRouter, Routes, Route } from "react-router-dom";
import SignupPage from "./components/SignUpPage/SignUpPage";
import LoginPage from "./components/LoginPage/LoginPage";
import HomePage from "./components/HomePage/HomePage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
         <Route path="/" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/home/:user" element={<HomePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
