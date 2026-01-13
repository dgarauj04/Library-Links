export interface User {
  id: number;
  username: string;
  email: string;
  avatar_url?: string;
  created_at: string;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  icon?: string; 
  description: string;
}

export interface Link {
  id: string;
  title: string;
  url: string;
  description: string;
  categoryId: string;
  faviconUrl?: string; 
  tags: string[];
}

export interface SearchState {
  query: string;
  isAiEnabled: boolean;
  isLoading: boolean;
}