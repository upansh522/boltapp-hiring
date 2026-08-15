import type { User } from "./user";

export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
}

export interface VerifyLoginCodeResponse {
  success: boolean;
  user: User;
  checkout_auth_token: string;
}
