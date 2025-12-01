import Input from "../ui/Input";
import Button from "../ui/Button";
import { useOrganization } from "../../context/OrganizationContext.jsx";
import { useState } from "react";

export default function Topbar() {
  const { organizationId, setOrganizationId } = useOrganization();
  const [value, setValue] = useState(organizationId || "");

  return (
    <header className="w-full bg-white/5 backdrop-blur border-b border-white/10 px-4 py-3 flex items-center justify-between">
      <div className="flex items-center gap-2">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-sky-500 text-white flex items-center justify-center font-bold shadow-lg shadow-indigo-500/30">
          OA
        </div>
        <div>
          <h1 className="text-base font-semibold text-slate-50">OkeAI Dashboard</h1>
          <p className="text-xs text-slate-300">CRM & AI Engine Playground</p>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <Input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="org-uuid"
          className="w-56"
        />
        <Button variant="secondary" onClick={() => setOrganizationId(value)}>
          Set Org
        </Button>
      </div>
    </header>
  );
}
