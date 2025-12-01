import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Card from "../components/ui/Card.jsx";
import Input from "../components/ui/Input.jsx";
import Button from "../components/ui/Button.jsx";
import { useAuth } from "../context/AuthContext.jsx";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await register(email, password, fullName);
      navigate("/inbox");
    } catch (err) {
      setError(err.response?.data || err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-slate-50 flex items-center justify-center px-4">
      <div className="grid grid-cols-1 md:grid-cols-2 w-full max-w-5xl gap-6">
        <div className="hidden md:flex flex-col justify-between glass-card rounded-2xl p-8 bg-white/5 border border-white/10">
          <div>
            <p className="text-xs uppercase tracking-[0.3em] text-indigo-200 font-semibold">OkeAI</p>
            <h2 className="text-3xl font-semibold mt-2">Daftar & Mulai</h2>
            <p className="text-sm text-slate-200/80 mt-2">
              Buat akun, dapatkan organisasi default, dan mulai uji AI Engine serta inbox WhatsApp/omnichannel.
            </p>
          </div>
          <div className="space-y-3 text-sm text-slate-200/90">
            <div className="flex items-center gap-3">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              <p>Org default otomatis dibuat saat register</p>
            </div>
            <div className="flex items-center gap-3">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              <p>AI Playground untuk prompt & RAG</p>
            </div>
            <div className="flex items-center gap-3">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              <p>Inbox sederhana dengan balasan AI</p>
            </div>
          </div>
        </div>

        <Card className="w-full max-w-lg mx-auto space-y-5">
          <div>
            <h1 className="text-2xl font-semibold text-slate-900">Register</h1>
            <p className="text-sm text-slate-600">Buat akun baru OkeAI.</p>
          </div>
          {error && <p className="text-sm text-red-600">Error: {JSON.stringify(error)}</p>}
          <form className="space-y-4" onSubmit={handleSubmit}>
            <div>
              <label className="text-sm font-medium text-slate-700">Nama Lengkap</label>
              <Input
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
                placeholder="Nama lengkap"
                className="mt-1"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-slate-700">Email</label>
              <Input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="you@example.com"
                className="mt-1"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-slate-700">Password</label>
              <Input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="********"
                className="mt-1"
              />
            </div>
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "Loading..." : "Register"}
            </Button>
          </form>
          <p className="text-sm text-slate-600">
            Sudah punya akun?{" "}
            <Link className="text-indigo-600 font-semibold" to="/login">
              Login
            </Link>
          </p>
        </Card>
      </div>
    </div>
  );
}
