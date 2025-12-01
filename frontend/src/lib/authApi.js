import http from "./axios";

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseKey = import.meta.env.VITE_SUPABASE_KEY;

const supabaseAuth = http.create({
  baseURL: supabaseUrl ? `${supabaseUrl}/auth/v1` : "/auth",
  headers: {
    apikey: supabaseKey || "",
    "Content-Type": "application/json",
  },
});

export const login = async (email, password) => {
  const { data } = await supabaseAuth.post("/token?grant_type=password", {
    email,
    password,
  });
  return data;
};

export const register = async (email, password, full_name) => {
  const { data } = await supabaseAuth.post("/signup", {
    email,
    password,
    data: { full_name },
  });
  return data;
};

export const logout = async () => {
  // local logout; Supabase logout requires refresh token; handled client side.
  return true;
};

export const getProfile = async () => {
  const { data } = await http.get("/auth/me");
  return data;
};

export const getOrganizations = async () => {
  const { data } = await http.get("/organization");
  return [data].filter(Boolean);
};
