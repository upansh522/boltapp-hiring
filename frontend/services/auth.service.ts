import api from "./api";

// Auth Service
export async function verifyLoginCode(data: {
  email: string;
  code: string;
}) {
  const response = await api.post("/api/auth/verify", data);
  return response.data;
}