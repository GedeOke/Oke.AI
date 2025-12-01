import { createContext, useContext, useEffect, useState } from "react";
import * as authApi from "../lib/authApi";

const AuthContext = createContext({
  token: null,
  user: null,
  organizations: [],
  currentOrganization: null,
  login: async () => {},
  register: async () => {},
  logout: () => {},
  setOrganization: () => {},
});

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [user, setUser] = useState(null);
  const [organizations, setOrganizations] = useState([]);
  const [currentOrganization, setCurrentOrganization] = useState(null);

  useEffect(() => {
    if (token) {
      localStorage.setItem("token", token);
      fetchProfile();
    } else {
      localStorage.removeItem("token");
      setUser(null);
    }
  }, [token]);

  const fetchProfile = async () => {
    try {
      const profile = await authApi.getProfile();
      setUser(profile);
      const orgs = await authApi.getOrganizations();
      setOrganizations(orgs);
      if (orgs?.length) {
        setCurrentOrganization(orgs[0]);
      }
    } catch (err) {
      console.error("Failed to fetch profile", err);
    }
  };

  const login = async (email, password) => {
    const data = await authApi.login(email, password);
    setToken(data.access_token);
    await fetchProfile();
  };

  const register = async (email, password, fullName) => {
    const data = await authApi.register(email, password, fullName);
    const accessToken = data?.session?.access_token;
    if (accessToken) {
      setToken(accessToken);
      await fetchProfile();
    }
  };

  const logout = async () => {
    await authApi.logout();
    setToken(null);
    setOrganizations([]);
    setCurrentOrganization(null);
  };

  const setOrganization = (org) => {
    setCurrentOrganization(org);
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        organizations,
        currentOrganization,
        login,
        register,
        logout,
        setOrganization,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
