import { Routes, Route, Navigate } from "react-router-dom";
import AiPlayground from "./pages/AiPlayground.jsx";
import Inbox from "./pages/Inbox.jsx";
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";
import { useAuth } from "./context/AuthContext.jsx";
import MainLayout from "./components/layout/MainLayout.jsx";
import Settings from "./pages/ai/Settings.jsx";
import KnowledgeBase from "./pages/ai/KnowledgeBase.jsx";
import Autopilot from "./pages/ai/Autopilot.jsx";
import SafetyRules from "./pages/ai/SafetyRules.jsx";
import Tools from "./pages/ai/Tools.jsx";
import Insights from "./pages/ai/Insights.jsx";
import { AiSettingsProvider } from "./context/AiSettingsContext.jsx";

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
            <AiSettingsProvider>
              <MainLayout>
                <AiPlayground />
              </MainLayout>
            </AiSettingsProvider>
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
      <Route
        path="/ai/settings"
        element={
          <ProtectedRoute>
            <AiSettingsProvider>
              <MainLayout>
                <Settings />
              </MainLayout>
            </AiSettingsProvider>
          </ProtectedRoute>
        }
      />
      <Route
        path="/ai/knowledge"
        element={
          <ProtectedRoute>
            <MainLayout>
              <KnowledgeBase />
            </MainLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/ai/autopilot"
        element={
          <ProtectedRoute>
            <MainLayout>
              <Autopilot />
            </MainLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/ai/safety"
        element={
          <ProtectedRoute>
            <MainLayout>
              <SafetyRules />
            </MainLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/ai/tools"
        element={
          <ProtectedRoute>
            <MainLayout>
              <Tools />
            </MainLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/ai/insights"
        element={
          <ProtectedRoute>
            <MainLayout>
              <Insights />
            </MainLayout>
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<Navigate to={token ? "/inbox" : "/login"} replace />} />
    </Routes>
  );
}

export default App;
