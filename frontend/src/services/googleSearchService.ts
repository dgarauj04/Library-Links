export interface SearchResult {
  id: string;
  title: string;
  url: string;
  description: string;
  snippet: string;
  favicon?: string;
}

interface GoogleSearchResponse {
  items?: Array<{
    title: string;
    link: string;
    snippet: string;
    displayLink: string;
  }>;
  searchInformation?: {
    totalResults: string;
  };
}

const initGoogleSearch = () => {
  const apiKey = import.meta.env.VITE_GOOGLE_API_KEY;
  const searchEngineId = import.meta.env.VITE_GOOGLE_SEARCH_ENGINE_ID;
  
  if (!apiKey || !searchEngineId) {
    console.error('Google API credentials not found');
    return null;
  }
  
  return { apiKey, searchEngineId };
};

/**
 * Busca links na web(Programmable Search Engine)
 * @param query - Termo de busca do usuário
 * @param category - Categoria para refinar a busca
 * @param numResults - Número de resultados (máximo 10)
 * @returns Array de resultados formatados
 */

export const searchWebLinks = async (
  query: string,
  numResults: number = 10
): Promise<SearchResult[]> => {
  const credentials = initGoogleSearch();
  if (!credentials) return [];
  
  if (!query.trim()) return [];

  try {
    const { apiKey, searchEngineId } = credentials;
    
    const url = new URL('https://www.googleapis.com/customsearch/v1');
    url.searchParams.append('key', apiKey);
    url.searchParams.append('cx', searchEngineId);
    url.searchParams.append('q', query);
    url.searchParams.append('num', Math.min(numResults, 10).toString());
    
    const response = await fetch(url.toString());
    
    if (!response.ok) {
      throw new Error(`Google Search API error: ${response.status}`);
    }
    
    const data: GoogleSearchResponse = await response.json();
    
    if (!data.items || data.items.length === 0) {
      return [];
    }
    
    const mappedResults = data.items.map((item, index) => ({
      id: `search-${Date.now()}-${index}`,
      title: item.title,
      url: item.link,
      description: item.snippet,
      snippet: item.snippet,
      favicon: `https://www.google.com/s2/favicons?domain=${item.displayLink}&sz=64`
    }));

    return filterResults(mappedResults);
    
  } catch (error) {
    console.error('Error searching web:', error);
    return [];
  }
};

export const searchByCategoryy = async (
  query: string,
  category: string
): Promise<SearchResult[]> => {
  const enhancedQuery = `${query} ${category}`;
  return searchWebLinks(enhancedQuery);
};

export const searchTools = async (
  toolType: string,
  additionalTerms: string = ''
): Promise<SearchResult[]> => {
  const query = `${toolType} tool ${additionalTerms}`.trim();
  return searchWebLinks(query);
};

const EXCLUDED_DOMAINS = [
  'reddit.com',
  'facebook.com',
  'twitter.com',
  'x.com',
  'instagram.com',
  'tiktok.com',
  'linkedin.com',
  'quora.com',
  'wikipedia.com',
  'news.ycombinator.com',
  'discord.com',
  'telegram.org',
  'whatsapp.com'
];

const EXCLUDED_KEYWORDS = [
  'discussão',
  'discussion',
  'fórum',
  'forum',
  'comunidade',
  'community',
  'debate',
  'opinião',
  'opinion',
  'existe alguma',
  'alguém sabe',
  'preciso de ajuda',
  'help needed',
  'pergunta',
  'question'
];

const filterResults = (results: SearchResult[]): SearchResult[] => {
  return results.filter(result => {
    const url = result.url.toLowerCase();
    const title = result.title.toLowerCase();
    const description = result.description.toLowerCase();
    
    const isExcludedDomain = EXCLUDED_DOMAINS.some(domain => 
      url.includes(domain)
    );
    
    const hasExcludedKeywords = EXCLUDED_KEYWORDS.some(keyword => 
      title.includes(keyword) || description.includes(keyword)
    );
    
    return !isExcludedDomain && !hasExcludedKeywords;
  });
};