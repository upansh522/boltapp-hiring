import api from "./api";

// User Service
export async function registerUser(userData: {
  email: string;
  first_name: string;
  last_name: string;
}) {
  const response = await api.post("/api/users/register", userData);
  return response.data;
}

export async function recognizeUser(email: string, signal?: AbortSignal) {
  const response = await api.get("/api/users/recognize", {
    params: { email },
    signal,
  });
  return response.data;
}
