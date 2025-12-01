import Input from "../ui/Input";
import Button from "../ui/Button";
import { useOrganization } from "../../context/OrganizationContext.jsx";
import { useState } from "react";

export default function Topbar() {
  const { organizationId, setOrganizationId } = useOrganization();
  const [value, setValue] = useState(organizationId || "");

  return (
    <header className="w-full bg-white border-b border-gray-200 px-4 py-3 flex items-center gap-3">
      <div className="flex items-center gap-2 w-full md:w-auto">
        <span className="text-sm font-medium text-gray-700">Organization ID</span>
        <div className="flex items-center gap-2">
          <Input
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder="org-uuid"
            className="w-56"
          />
          <Button variant="secondary" onClick={() => setOrganizationId(value)}>
            Set
          </Button>
        </div>
      </div>
    </header>
  );
}
