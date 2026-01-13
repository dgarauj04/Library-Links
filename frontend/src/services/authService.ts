import api from './api';
import { type User } from '../types';

let currentToken: string | null = null;
let currentUser: User | null = null;

interface RegisterResponse {
  access_token: string;
  token_type: string;
  user: User;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export const registerUser = async (
  username: string,
  email: string,
  password: string
): Promise<{ success: boolean; message: string; user?: User }> => {
  try {
    const response = await api.post<RegisterResponse>('/auth/register', {
      username,
      email,
      password,
    });

    const { access_token, user } = response.data;
    currentToken = access_token;
    currentUser = user;
    
    return {
      success: true,
      message: 'Conta criada com sucesso!',
      user,
    };
  } catch (error: any) {
    const message =
      error.response?.data?.detail || 'Erro ao criar conta. Tente novamente.';
    return { success: false, message };
  }
};

export const loginUser = async (
  identifier: string,
  password: string
): Promise<{ success: boolean; user?: User; message: string }> => {
  try {
    const response = await api.post<LoginResponse>('/auth/login', {
      identifier,
      password,
    });

    const { access_token, user } = response.data;
    
    currentToken = access_token;
    currentUser = user;
  

    return {
      success: true,
      user,
      message: 'Login realizado com sucesso!',
    };
  } catch (error: any) {
    const message =
      error.response?.data?.detail || 'Credenciais inválidas.';
    return { success: false, message };
  }
};

export const logoutUser = () => {
  currentToken = null;
  currentUser = null;
};

export const getCurrentUser = (): User | null => {
  return currentUser;
};

export const getToken = (): string | null => {
  return currentToken;
};

export const isAuthenticated = (): boolean => {
  const hasToken = !!currentToken;
  return hasToken;
};