import axios from "axios";

// Centralized Axios instance
const api = axios.create({
  // This is public browser configuration, not a secret. Configure it per
  // environment in .env.local; deployed builds receive their API URL at build time.
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || undefined,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
