import { Routes, Route, Navigate } from "react-router-dom";
import AiPlayground from "./pages/AiPlayground.jsx";
import Inbox from "./pages/Inbox.jsx";
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";
import { useAuth } from "./context/AuthContext.jsx";
import MainLayout from "./components/layout/MainLayout.jsx";

function App() {
  const { token } = useAuth();

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route
        path="/ai"
        element={
          <ProtectedRoute>
            <MainLayout>
              <AiPlayground />
            </MainLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/inbox"
        element={
          <ProtectedRoute>
            <MainLayout>
              <Inbox />
            </MainLayout>
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<Navigate to={token ? "/inbox" : "/login"} replace />} />
    </Routes>
  );
}

export default App;
