import type { User } from "./user";

export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
}
