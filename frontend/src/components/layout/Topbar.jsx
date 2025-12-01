import Input from "../ui/Input";
import Button from "../ui/Button";
import { useOrganization } from "../../context/OrganizationContext.jsx";
import { useState } from "react";
import { useAuth } from "../../context/AuthContext.jsx";

export default function Topbar({ onToggleSidebar }) {
  const { organizationId, setOrganizationId } = useOrganization();
  const { user, logout } = useAuth();
  const [value, setValue] = useState(organizationId || "");

  return (
    <header className="w-full bg-white shadow-sm border-b border-slate-200 px-4 py-3 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <button
          className="md:hidden rounded-lg border border-slate-200 p-2 hover:bg-slate-100"
          onClick={onToggleSidebar}
        >
          ☰
        </button>
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-blue-500 text-white flex items-center justify-center font-bold shadow-md">
          OA
        </div>
        <div>
          <h1 className="text-base font-semibold text-slate-900">OkeAI Dashboard</h1>
          <p className="text-xs text-slate-500">CRM & AI Engine Playground</p>
        </div>
      </div>
      <div className="flex items-center gap-3">
        <Input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="organization id"
          className="w-52"
        />
        <Button variant="secondary" onClick={() => setOrganizationId(value)}>
          Set Org
        </Button>
        {user && (
          <div className="hidden md:flex items-center gap-2 text-sm text-slate-600">
            <div className="text-right">
              <div className="font-semibold text-slate-800">{user.email}</div>
              <div className="text-xs text-slate-500">Signed in</div>
            </div>
            <Button variant="ghost" onClick={logout}>
              Logout
            </Button>
          </div>
        )}
      </div>
    </header>
  );
}
