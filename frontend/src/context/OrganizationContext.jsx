import { createContext, useContext, useState } from "react";

const OrganizationContext = createContext({ organizationId: "", setOrganizationId: () => {} });

export const OrganizationProvider = ({ children }) => {
  const [organizationId, setOrganizationId] = useState("");

  return (
    <OrganizationContext.Provider value={{ organizationId, setOrganizationId }}>
      {children}
    </OrganizationContext.Provider>
  );
};

export const useOrganization = () => useContext(OrganizationContext);
