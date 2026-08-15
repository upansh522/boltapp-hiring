export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
}

export interface RegisterResponse {
  success: boolean;
  user: User;
  code: string;
  message: string;
}

export interface RecognitionResponse {
  success: boolean;
  registered: boolean;
  user?: User;
}