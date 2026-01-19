<script setup lang="ts">
import { ref, watch } from 'vue';
import { Search, Sparkles, X, Loader2 } from 'lucide-vue-next';
import { useDebounceFn } from '@vueuse/core';

interface SearchBarProps {
  isLoading?: boolean;
}

const props = withDefaults(defineProps<SearchBarProps>(), {
  isLoading: false
});

const emit = defineEmits<{
  search: [query: string, isAi: boolean];
}>();

const query = ref('');
const isAiMode = ref(false);

const debouncedSearch = useDebounceFn((value: string) => {
  if (!isAiMode.value) {
    emit('search', value, false);
  }
}, 500);

watch(query, (newQuery) => {
  debouncedSearch(newQuery);
});

const keyDown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && isAiMode.value) {
    emit('search', query.value, true);
  }
};

const clearSearch = () => {
  query.value = '';
  emit('search', '', isAiMode.value);
};

const toggleAiMode = () => {
  isAiMode.value = !isAiMode.value;
  if (!isAiMode.value) {
    emit('search', query.value, false);
  }
};
</script>

<template>
  <div class="w-full max-w-6xl mx-auto relative z-20">
    <div 
      :class="[
        'relative flex items-center w-full rounded-2xl transition-all duration-300 border backdrop-blur-xl',
        isAiMode 
          ? 'bg-linear-to-r from-purple-500/10 via-pink-500/10 to-cyan-500/10 border-purple-500/50 shadow-[0_0_30px_rgba(168,85,247,0.2)]' 
          : 'bg-white/80 border-white/60 shadow-[0_8px_30px_rgba(0,0,0,0.04)] dark:bg-white/5 dark:border-white/10 dark:shadow-xl'
      ]"
    >
      <div class="pl-4 pr-3 text-gray-400">
        <Loader2 v-if="isLoading" class="animate-spin text-cyan-400" :size="20" />
        <Sparkles v-else-if="isAiMode" class="text-purple-500 dark:text-purple-400 animate-pulse" :size="20" />
        <Search v-else :size="20" />
      </div>

      <input
        v-model="query"
        type="text"
        @keydown="keyDown"
        :placeholder="isAiMode ? 'Buscar na web: \'paleta de cores ferramenta\', \'framework Vue componentes\'...' : 'Pesquisar na biblioteca...'"
        class="w-full bg-transparent border-none focus:ring-0 py-4 pr-12 text-lg
               font-medium text-slate-800 placeholder-slate-400
               dark:text-white dark:placeholder-gray-500"
      />

      <div class="absolute right-3 flex items-center space-x-2">
        <button 
          v-if="query" 
          @click="clearSearch" 
          class="p-1 hover:bg-black/5 dark:hover:bg-white/10 rounded-full text-gray-400 transition-colors"
        >
          <X :size="16" />
        </button>
        
        <div class="h-6 w-px bg-slate-200 dark:bg-white/10 mx-2" />

        <button
          @click="toggleAiMode"
          :class="[
            'flex items-center space-x-1 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all duration-300',
            isAiMode 
              ? 'bg-purple-500 text-white shadow-lg shadow-purple-500/30' 
              : 'bg-slate-100 text-slate-500 hover:bg-slate-200 hover:text-slate-800 dark:bg-white/5 dark:text-gray-400 dark:hover:bg-white/10 dark:hover:text-white'
          ]"
        >
          <Sparkles :size="12" :class="{ 'fill-current': isAiMode }" />
          <span>Busca Web</span>
        </button>
      </div>
    </div>
    
    <div 
      :class="[
        'mt-2 flex justify-between px-4 text-xs transition-opacity duration-300',
        query ? 'opacity-100' : 'opacity-0'
      ]"
    >
      <span class="text-purple-400/40 font-medium">
        {{ isAiMode ? 'Pressione Enter para buscar na web' : 'Buscando na biblioteca...' }}
      </span>
      <span v-if="isAiMode" class="text-purple-600 dark:text-purple-400 font-bold">
        Powered by Google
      </span>
    </div>
  </div>
</template>

<style scoped>
input:focus {
  outline: none;
}
</style>