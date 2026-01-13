import api from './api';
import { type Category, type Link } from '../types';

let categoriesCache: Category[] | null = null;
let linksCache: Link[] | null = null;


export const getCategories = async (): Promise<Category[]> => {
  try {
    if (categoriesCache) {
      return categoriesCache;
    }

    const response = await api.get<Category[]>('/categories');
    
    categoriesCache = response.data;
    
    return categoriesCache;
  } catch (error) {
    return [];
  }
};

export const addCategory = async (name: string): Promise<Category> => {
  try {
    const response = await api.post<Category>('/categories', {
      name,
      slug: name.toLowerCase().replace(/\s+/g, '-'),
      description: ''
    });

    const newCategory = response.data;
    
    if (categoriesCache) {
      categoriesCache.push(newCategory);
    }
    
    return newCategory;
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Erro ao criar categoria');
  }
};

export const deleteCategory = async (id: string): Promise<void> => {
  try {
    await api.delete(`/categories/${id}`);
    
    if (categoriesCache) {
      categoriesCache = categoriesCache.filter(c => c.id !== id);
    }
    
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Erro ao deletar categoria');
  }
};

const convertLinkFromAPI = (apiLink: any): Link => {
  return {
    id: apiLink.id,
    title: apiLink.title,
    url: apiLink.url,
    description: apiLink.description,
    faviconUrl: apiLink.favicon_url,
    tags: apiLink.tags || [],
    categoryId: apiLink.categoryId || apiLink.category_id 
  };
};

const convertLinkToAPI = (link: Omit<Link, 'id'> | Link): any => {
  return {
    title: link.title,
    url: link.url,
    description: link.description,
    favicon_url: link.faviconUrl,
    tags: link.tags,
    category_id: link.categoryId
  };
};

export const getLinks = async (): Promise<Link[]> => {
  try {
    if (linksCache) {
      return linksCache;
    }

    const response = await api.get('/links');
    
    linksCache = response.data.map(convertLinkFromAPI);
    
    return linksCache;
  } catch (error) {
    return [];
  }
};

export const addLink = async (link: Omit<Link, 'id'>): Promise<Link> => {
  try {
    const response = await api.post('/links', convertLinkToAPI(link));
    const newLink = convertLinkFromAPI(response.data);
    
    if (linksCache) {
      linksCache.push(newLink);
    }
    
    return newLink;
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Erro ao criar link');
  }
};

export const updateLink = async (id: string, updates: Partial<Link>): Promise<Link> => {
  try {
    const response = await api.put(`/links/${id}`, convertLinkToAPI(updates as Link));
    const updatedLink = convertLinkFromAPI(response.data);
    
    if (linksCache) {
      const index = linksCache.findIndex(l => l.id === id);
      if (index !== -1) {
        linksCache[index] = updatedLink;
      }
    }
    
    return updatedLink;
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Erro ao atualizar link');
  }
};

export const deleteLink = async (id: string): Promise<void> => {
  try {
    await api.delete(`/links/${id}`);
    
    if (linksCache) {
      linksCache = linksCache.filter(l => l.id !== id);
    }
    
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Erro ao deletar link');
  }
};

export const clearCache = () => {
  categoriesCache = null;
  linksCache = null;
};

export const refreshData = async (): Promise<void> => {
  clearCache();
  await Promise.all([getCategories(), getLinks()]);
};
