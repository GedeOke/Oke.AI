import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Card from "../components/ui/Card.jsx";
import Input from "../components/ui/Input.jsx";
import Button from "../components/ui/Button.jsx";
import { useAuth } from "../context/AuthContext.jsx";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await login(email, password);
      navigate("/inbox");
    } catch (err) {
      setError(err.response?.data || err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-slate-50 flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-2 gap-6 items-center">
        <div className="glass-card rounded-3xl p-8 space-y-5 shadow-2xl border border-white/10">
          <p className="text-xs uppercase tracking-[0.25em] text-indigo-200 font-semibold">O K E A I</p>
          <h2 className="text-3xl lg:text-4xl font-bold">CRM + AI Engine</h2>
          <p className="text-base text-slate-200/85">
            Kelola percakapan, jalankan AI Playground, dan otomatisasi balasan pelanggan dalam satu dashboard.
          </p>
          <div className="space-y-3 text-sm text-slate-200/90">
            <div className="flex items-center gap-3">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              <p>RAG + multi-provider LLM siap pakai</p>
            </div>
            <div className="flex items-center gap-3">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              <p>Inbox terpadu & webhook WhatsApp</p>
            </div>
            <div className="flex items-center gap-3">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              <p>Autopilot & agent assist suggestions</p>
            </div>
          </div>
        </div>

        <div className="glass-card rounded-3xl p-8 shadow-2xl border border-white/10 bg-gradient-to-br from-slate-900/60 to-slate-800/60">
          <div className="space-y-1 mb-6">
            <h1 className="text-2xl font-semibold text-white">Login</h1>
            <p className="text-sm text-slate-300">Masuk ke dashboard OkeAI untuk mulai bekerja.</p>
          </div>
          {error && <p className="text-sm text-red-300 mb-4">Error: {JSON.stringify(error)}</p>}
          <form className="space-y-4" onSubmit={handleSubmit}>
            <div className="space-y-1">
              <label className="text-sm font-medium text-slate-200">Email</label>
              <Input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="you@example.com"
                className="mt-1 bg-white text-slate-900"
              />
            </div>
            <div className="space-y-1">
              <label className="text-sm font-medium text-slate-200">Password</label>
              <Input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="********"
                className="mt-1 bg-white text-slate-900"
              />
            </div>
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "Loading..." : "Login"}
            </Button>
          </form>
          <p className="text-sm text-slate-300 mt-4">
            Belum punya akun?{" "}
            <Link className="text-indigo-300 font-semibold" to="/register">
              Register
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
