<script setup lang="ts">
import { ref } from 'vue';
import { X, FolderOpen, Trash2 } from 'lucide-vue-next';
import ConfirmCard from './ConfirmCard.vue';

export interface Category {
  id: string;
  name: string;
  slug: string;
  icon?: string;
  description: string;
}

export interface Link {
  id:string;
  categoryId: string;
  [key: string]: any;
}

interface CategoryManagerProps {
  isOpen: boolean;
  categories: Category[];
  links: Link[];
}

const props = defineProps<CategoryManagerProps>();

const emit = defineEmits<{
  close: [];
  deleteCategory: [id: string];
}>();

const isConfirmOpen = ref(false);
const categoryToDelete = ref<Category | null>(null);

const closeModal = () => {
  emit('close');
};

const getLinkCount = (categoryId: string): number => {
  return props.links.filter(link => link.categoryId === categoryId).length;
};

const deleteCategory = (category: Category) => {
  const linkCount = getLinkCount(category.id);
  
  if (linkCount > 0) {
    alert(`Não é possível deletar "${category.name}" porque ela possui ${linkCount} ${linkCount === 1 ? 'link' : 'links'}. Delete os links primeiro.`);
    return;
  }
  
  categoryToDelete.value = category;
  isConfirmOpen.value = true;
};

const confirmDelete = () => {
  if (categoryToDelete.value) {
    emit('deleteCategory', categoryToDelete.value.id);
  }
  isConfirmOpen.value = false;
  categoryToDelete.value = null;
};

const cancelDelete = () => {
  isConfirmOpen.value = false;
  categoryToDelete.value = null;
};
</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div 
          class="absolute inset-0 bg-black/40 backdrop-blur-xs transition-opacity" 
          @click="closeModal"
        />
        
        <div 
          class="relative w-full max-w-2xl transform rounded-2xl border border-white/20 
                 p-6 shadow-2xl transition-all max-h-[80vh] overflow-y-auto
                 bg-slate-900/80 backdrop-blur-xl text-white"
        >
          <button 
            @click="closeModal"
            class="absolute right-4 top-4 rounded-full p-1 text-gray-400 hover:bg-white/10"
          >
            <X :size="20" />
          </button>

          <h2 class="mb-6 text-2xl font-bold flex items-center gap-2">
            <FolderOpen class="text-cyan-500" />
            Gerenciar Categorias
          </h2>

          <div 
            v-if="categories.length === 0"
            class="text-center py-12 rounded-xl border border-dashed
                   bg-white/5 border-white/10"
          >
            <p class="text-gray-400 font-medium">
              Nenhuma categoria encontrada. Crie uma nova categoria ao adicionar um link.
            </p>
          </div>

          <div v-else class="space-y-3">
            <div
              v-for="category in categories"
              :key="category.id"
              class="flex items-center justify-between p-4 rounded-xl border
                      hover:shadow-md bg-white/5 border-white/10 hover:bg-white/10 transition-all"
            >
              <div class="flex items-center gap-3 flex-1">
                <div 
                  class="w-10 h-10 rounded-xl flex items-center justify-center
                         border border-cyan-500/20 
                         bg-linear-to-br via-none from-cyan-500/20 to-blue-500/20"
                >
                  <FolderOpen :size="20" class="text-cyan-600 dark:text-cyan-400" />
                </div>
                
                <div class="flex-1">
                  <h3 class="font-bold text-slate-800 dark:text-white">
                    {{ category.name }}
                  </h3>
                  <p class="text-xs text-slate-500 dark:text-gray-400">
                    {{ getLinkCount(category.id) }} {{ getLinkCount(category.id) === 1 ? 'link' : 'links' }}
                  </p>
                </div>
              </div>

              <button
                @click="deleteCategory(category)"
                :disabled="getLinkCount(category.id) > 0"
                :class="[
                  'p-2 rounded-lg transition-colors',
                  getLinkCount(category.id) > 0
                    ? 'text-slate-300 dark:text-gray-600 cursor-not-allowed'
                    : 'text-slate-400 hover:text-red-600 hover:bg-red-50 dark:text-white/40 dark:hover:text-red-400 dark:hover:bg-red-500/10'
                ]"
                :title="getLinkCount(category.id) > 0 ? 'Delete os links desta categoria primeiro' : 'Deletar categoria'"
              >
                <Trash2 :size="20" />
              </button>
            </div>
          </div>

          <div class="mt-6 p-4 rounded-xl bg-blue-500/10 border border-blue-500/20">
            <p class="text-sm text-blue-300">
              <strong>💡 Dica:</strong> Você não pode deletar categorias que possuem links. 
              Delete os links primeiro ou mova-os para outra categoria.
            </p>
          </div>

          <div class="mt-6 flex justify-end">
            <button
              @click="closeModal"
              class="px-6 py-2.5 rounded-xl bg-pink-700
                     font-bold text-white shadow-lg shadow-pink-500/25 transition-all 
                     hover:shadow-pink-500/40 hover:-translate-y-0.5"
            >
              Fechar
            </button>
          </div>
        </div>
      </div>
    </Transition>
    <ConfirmCard
      :show="isConfirmOpen"
      title="Deletar Categoria"
      :message="`Tem certeza que deseja deletar a categoria '${categoryToDelete?.name}'?`"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
    />
  </Teleport>
</template>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active > div:last-child,
.modal-leave-active > div:last-child {
  transition: transform 0.3s ease;
}

.modal-enter-from > div:last-child,
.modal-leave-to > div:last-child {
  transform: scale(0.9);
}
</style>