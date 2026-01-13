<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { Plus, LogOut, FolderOpen, Globe } from 'lucide-vue-next';
import LinkCard from '../components/LinkCard.vue';
import SearchBar from '../components/SearchBar.vue';
import AddLinkModal, { type Category, type Link } from '../components/AddLinkModal.vue';
import CategoryManager from '../components/CategoryManager.vue';
import { getCategories, getLinks, addLink, addCategory, deleteLink, deleteCategory } from '../services/storageService';
import { searchWebLinks, type SearchResult } from '../services/googleSearchService';
import { logoutUser } from '../services/authService';

const router = useRouter();
const categories = ref<Category[]>([]);
const links = ref<Link[]>([]);
const filteredLinks = ref<Link[]>([]);
const webSearchResults = ref<SearchResult[]>([]);
const isLoading = ref(true);
const activeCategory = ref('all');
const searchState = ref({
  query: '',
  isAi: false,
  loading: false,
  isWebSearch: false 
});
const addModalOpen = ref(false);
const categoryManagerOpen = ref(false);

const displayedLinks = computed(() => {
  if (searchState.value.isWebSearch && webSearchResults.value.length > 0) {
    return webSearchResults.value.map(result => ({
      id: result.id,
      title: result.title,
      url: result.url,
      description: result.description,
      categoryId: 'web-search',
      tags: ['Resultado da Web']
    }));
  }
  
  if (searchState.value.query && !searchState.value.isWebSearch) {
    return filteredLinks.value;
  }
  if (activeCategory.value === 'all') {
    return links.value;
  }
  return links.value.filter(l => l.categoryId === activeCategory.value);
});

const resultTitle = computed(() => {
  if (searchState.value.isWebSearch) {
    return `Resultados da Web para "${searchState.value.query}"`;
  }
  if (searchState.value.query) {
    return `Resultados na Biblioteca para "${searchState.value.query}"`;
  }
  if (activeCategory.value === 'all') {
    return 'Recursos em Destaque';
  }
  return categories.value.find(c => c.id === activeCategory.value)?.name || '';
});

const loadData = async () => {
  try {
    isLoading.value = true;
    const [fetchedCategories, fetchedLinks] = await Promise.all([
      getCategories(),
      getLinks()
    ]);
    
    categories.value = fetchedCategories;
    links.value = [...fetchedLinks].reverse();
  } catch (error) {
    categories.value = [];
    links.value = [];
  } finally {
    isLoading.value = false;
  }
};

const inputSearch = async (query: string, isAi: boolean) => {
  searchState.value = { 
    query, 
    isAi, 
    loading: isAi && !!query,
    isWebSearch: false 
  };
  
  webSearchResults.value = [];

  if (!query) {
    filteredLinks.value = [];
    searchState.value.loading = false;
    return;
  }

  if (isAi) {
    searchState.value.loading = true;
    searchState.value.isWebSearch = true;
    
    const results = await searchWebLinks(query, 10);
    webSearchResults.value = results;
    
    searchState.value.loading = false;
  } else {
    const lowerQuery = query.toLowerCase();
    filteredLinks.value = links.value.filter(link => 
      link.title.toLowerCase().includes(lowerQuery) ||
      link.description.toLowerCase().includes(lowerQuery) ||
      link.tags.some(tag => tag.toLowerCase().includes(lowerQuery))
    );
  }
};

const btnLogout = () => {
  logoutUser();
  router.push('/login');
};

const linkAdded = async (newLink: Link, categoryName: string) => {
  let categoryIdToUse = '';
  const existingCategory = categories.value.find(
    c => c.name.toLowerCase() === categoryName.toLowerCase()
  );

  if (existingCategory) {
    categoryIdToUse = existingCategory.id;
  } else {
    const newCat = await addCategory(categoryName);
    categoryIdToUse = newCat.id;
  }

  const linkToAdd = { ...newLink, categoryId: categoryIdToUse };
  await addLink(linkToAdd);
  
  await loadData();
};

const btnDeleteLink = async (linkId: string) => {
  await deleteLink(linkId);
  await loadData();
};

const btnDeleteCategory = async (categoryId: string) => {
  await deleteCategory(categoryId);
  await loadData();

  if (activeCategory.value === categoryId) {
    activeCategory.value = 'all';
  }
};

onMounted(() => {
  loadData();
});
</script>

<template>
  <div class="space-y-6 pb-12">
    <div class="text-center space-y-6 pt-10 px-4">
      <h1 
        class="text-4xl md:text-6xl font-extrabold tracking-tight text-transparent 
        bg-clip-text bg-linear-to-r from-slate-200 via-cyan-200 to-gray-200">
        Library Links<br/> Biblioteca para Seus links favoritos.
      </h1>
      <p class="text-lg max-w-2xl mx-auto text-gray-400 font-medium">
        Explore sua biblioteca de links ou busque novos recursos na web com busca inteligente.
      </p>
      
      <div class="mt-8">
        <SearchBar 
          :is-loading="searchState.loading" 
          @search="inputSearch" 
        />
      </div>
      
      <div 
        v-if="searchState.isWebSearch"
        class="flex items-center justify-center gap-2 text-sm font-medium text-purple-400"
      >
        <Globe :size="16" class="animate-pulse" />
        <span>Buscando na Web</span>
      </div>
    </div>

    <div 
      v-if="!searchState.query" 
      class="flex overflow-x-auto pb-4 gap-2 no-scrollbar justify-center flex-wrap px-4"
    >
      <button
        @click="activeCategory = 'all'"
        :class="[
          'px-5 py-2.5 rounded-full text-sm font-medium whitespace-nowrap transition-all border capitalize',
          activeCategory === 'all' 
            ? 'bg-white shadow-cyan-500/10 text-gray-900 border-white/20 shadow-[0_0_20px_rgba(255,255,255,0.3)]' 
            : 'hover:shadow-md hover:border-slate-200 bg-white/5 border-white/5 text-gray-400 hover:bg-white/10 hover:text-white'
        ]"
      >
        Todos
      </button>
      
      <button
        v-for="cat in categories"
        :key="cat.id"
        @click="activeCategory = cat.id"
        :class="[
          'px-5 py-2.5 rounded-full text-sm font-medium whitespace-nowrap transition-all border capitalize',
          activeCategory === cat.id 
            ? 'border-cyan-500/50 bg-cyan-500/20 text-cyan-100 shadow-[0_0_20px_rgba(34,211,238,0.2)]' 
            : 'text-slate-600  hover:text-white hover:shadow-md hover:border-slate-200 bg-white/5 border-white/5 dark:text-gray-400 hover:bg-white/10'
        ]"
      >
        {{ cat.name }}
      </button>
    </div>

    <div class="space-y-4 px-2">
      <div class="flex items-center justify-between">
        <h2 class="text-2xl font-bold text-white">
          {{ resultTitle }}
        </h2>
        <span class="text-sm font-medium text-gray-500">
          {{ displayedLinks.length }} {{ displayedLinks.length === 1 ? 'item' : 'itens' }}
        </span>
      </div>

      <div v-if="isLoading" class="flex items-center justify-center py-20">
        <div class="text-center space-y-4">
          <div class="w-16 h-16 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin mx-auto" />
          <p class="text-gray-400">Carregando recursos...</p>
        </div>
      </div>

      <div 
        v-else-if="displayedLinks.length === 0 && !searchState.loading" 
        class="text-center py-20 rounded-3xl border border-dashed
               dark:bg-white/5 dark:border-white/5"
      >
        <p class="text-gray-400 font-medium">
          {{ searchState.isWebSearch 
            ? 'Nenhum resultado encontrado na web. Tente termos diferentes.' 
            : 'Nenhum recurso encontrado. Tente um termo diferente.' 
          }}
        </p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <LinkCard 
          v-for="link in displayedLinks" 
          :key="link.id" 
          :link="link"
          @delete="btnDeleteLink"
        />
      </div>
    </div>

    <button
      @click="btnLogout"
      class="fixed bottom-8 left-8 z-40 flex h-14 w-14 items-center justify-center 
             rounded-full bg-red-600 text-white shadow-xl shadow-red-500/30 
             transition-transform hover:scale-110 hover:bg-red-700 focus:outline-none"
      aria-label="Sair da conta"
      title="Sair da conta"
    >
      <LogOut :size="24" />
    </button>

    <button
      @click="categoryManagerOpen = true"
      class="fixed bottom-24 right-8 z-40 flex h-14 w-14 items-center justify-center 
             rounded-full bg-pink-700 text-white shadow-xl shadow-purple-500/30 transition-transform
              hover:scale-110 hover:shadow-purple-500/50 focus:outline-none"
      aria-label="Gerenciar Categorias"
      title="Gerenciar Categorias"
    >
      <FolderOpen :size="24" />
    </button>

    <button
      @click="addModalOpen = true"
      class="fixed bottom-8 right-8 z-40 flex h-14 w-14 items-center justify-center 
             rounded-full bg-blue-500 text-white shadow-xl shadow-cyan-500/30 transition-transform 
             hover:scale-110 hover:shadow-cyan-500/50 focus:outline-none"
      aria-label="Adicionar Link"
      title="Adicionar Novo Recurso"
    >
      <Plus :size="28" />
    </button>

    <AddLinkModal 
      :is-open="addModalOpen" 
      :categories="categories"
      @close="addModalOpen = false" 
      @success="linkAdded"
    />

    <CategoryManager
      :is-open="categoryManagerOpen"
      :categories="categories"
      :links="links"
      @close="categoryManagerOpen = false"
      @delete-category="btnDeleteCategory"
    />
  </div>
</template>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}

.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>