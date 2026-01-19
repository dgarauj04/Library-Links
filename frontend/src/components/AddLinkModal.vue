<script setup lang="ts">
import { ref, watch } from 'vue';
import { X, Plus, Save } from 'lucide-vue-next';

export interface Category {
  id: string;
  name: string;
}

export interface Link {
  id: string;
  title: string;
  url: string;
  description: string;
  categoryId: string;
  tags: string[];
}

interface AddLinkModalProps {
  isOpen: boolean;
  categories: Category[];
}

const props = defineProps<AddLinkModalProps>();

const emit = defineEmits<{
  close: [];
  success: [link: Link, categoryName: string];
}>();

const formData = ref({
  title: '',
  url: '',
  description: '',
  categoryName: '',
  tags: ''
});

watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    formData.value = {
      title: '',
      url: '',
      description: '',
      categoryName: '',
      tags: ''
    };
  }
});

const closeModal = () => {
  emit('close');
};

const btnSubmit = () => {
  if (!formData.value.categoryName.trim()) {
    alert("Por favor, informe uma categoria.");
    return;
  }

  const newLink: Link = {
    id: Date.now().toString(),
    title: formData.value.title,
    url: formData.value.url,
    description: formData.value.description,
    categoryId: '', 
    tags: formData.value.tags
      .split(',')
      .map(t => t.trim())
      .filter(t => t.length > 0)
  };

  emit('success', newLink, formData.value.categoryName.trim());
  closeModal();
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
          class="relative w-full max-w-lg transform rounded-2xl border border-white/20 
                 p-6 shadow-2xl transition-all
                 bg-slate-900/80 backdrop-blur-xl text-white"
        >
          <button 
            @click="closeModal"
            class="absolute right-4 top-4 rounded-full p-1 text-gray-400 hover:bg-white/10"
          >
            <X :size="20" />
          </button>

          <h2 class="mb-6 text-2xl font-bold flex items-center gap-2">
            <Plus class="text-cyan-500" />
            Adicionar Novo Recurso
          </h2>

          <form @submit.prevent="btnSubmit" class="space-y-4">
            <div>
              <label class="mb-1 block text-sm font-medium text-slate-300">
                Nome do Site / Ferramenta
              </label>
              <input
                v-model="formData.title"
                required
                type="text"
                class="w-full rounded-xl border px-4 py-3 
                       focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 
                       border-white/10 bg-black/20 text-white"
                placeholder="Ex: Figma"
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium text-slate-300">
                URL
              </label>
              <input
                v-model="formData.url"
                required
                type="url"
                class="w-full rounded-xl border px-4 py-3 
                       focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 
                       border-white/10 bg-black/20 text-white"
                placeholder="https://..."
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium text-slate-300">
                Categoria
              </label>
              <input
                v-model="formData.categoryName"
                required
                list="categories-list"
                type="text"
                class="w-full rounded-xl border px-4 py-3 
                       focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 
                       border-white/10 bg-black/20 text-white"
                placeholder="Selecione ou digite uma nova..."
              />
              <datalist id="categories-list">
                <option v-for="category in categories" :key="category.id" :value="category.name" />
              </datalist>
              <p class="mt-1 text-xs text-slate-400">
                Digite um nome novo para criar automaticamente.
              </p>
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium text-slate-300">
                Descrição
              </label>
              <textarea
                v-model="formData.description"
                required
                rows="3"
                class="w-full rounded-xl border px-4 py-3 
                       focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 
                       border-white/10 bg-black/20 text-white"
                placeholder="O que essa ferramenta faz?"
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium text-slate-300">
                Tags (separadas por vírgula)
              </label>
              <input
                v-model="formData.tags"
                type="text"
                class="w-full rounded-xl border px-4 py-3 
                       focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 
                       border-white/10 bg-black/20 text-white"
                placeholder="design, cores, gratuito"
              />
            </div>

            <div class="mt-6 flex gap-3">
              <button
                type="button"
                @click="closeModal"
                class="flex-1 rounded-xl py-3 font-medium bg-red-300/10 text-white 
                       hover:bg-red-500/20 transition-colors"
              >
                Cancelar
              </button>
              <button
                type="submit"
                class="flex-1 flex items-center justify-center gap-2 rounded-xl 
                        bg-cyan-600 py-3 font-bold text-white 
                       shadow-lg shadow-cyan-500/250 transition-all hover:shadow-cyan-500/40 
                       hover:-translate-y-0.5"
              >
                <Save :size="18" /> Salvar Link
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>
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