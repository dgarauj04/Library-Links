<script setup lang="ts">
import { ref } from 'vue'
import { ExternalLink, Trash2 } from 'lucide-vue-next'
import ConfirmCard from './ConfirmCard.vue'

export interface Link {
  id: string;
  title: string;
  url: string;
  description: string;
  categoryId: string;
  tags: string[];
}

interface LinkCardProps {
  link: Link;
}

const props = defineProps<LinkCardProps>()

const emit = defineEmits<{
  delete: [id:string];
}>()

const showConfirm = ref(false)

const imageError = (e: Event) => {
  const target = e.target as HTMLImageElement
  target.style.display = 'none'
}

const btnDelete = () => {
  showConfirm.value = true
}

const confirmDelete = () => {
  emit('delete', props.link.id)
  showConfirm.value = false
}

const cancelDelete = () => {
  showConfirm.value = false
}
</script>

<template>
  <div 
    class="group relative flex flex-col justify-between p-6 rounded-3xl
           backdrop-blur-xl transition-all duration-300 ease-out border hover:-translate-y-1
           bg-white/5 border-white/10 shadow-xl hover:bg-white/10 hover:border-white/20 
           hover:shadow-[0_8px_32px_0_rgba(31,38,135,0.47)]"
  >
    <div 
      class="absolute -top-10 -right-10 w-24 h-24 rounded-full blur-2xl 
             transition-colors duration-500 pointer-events-none
             bg-cyan-500/20 group-hover:bg-cyan-400/30" 
    />

    <div>
      <div class="flex justify-between items-start mb-4">
        <div class="flex items-center space-x-3 flex-1">
          <div 
            class="w-10 h-10 rounded-2xl flex items-center justify-center bg-linear-to-br 
                   via-none from-indigo-500/20 to-purple-500/20 border border-white/10 shadow-none"
          >
            <img 
              :src="`https://www.google.com/s2/favicons?domain=${link.url}&sz=64`" 
              :alt="`${link.title} favicon`" 
              class="w-5 h-5 opacity-80"
              @error="imageError"
            />
          </div>
          <h3 class="text-xl font-bold tracking-tight text-white">
            {{ link.title }}
          </h3>
        </div>
        
        <div class="flex items-center gap-2">
          <a 
            :href="link.url" 
            target="_blank" 
            rel="noopener noreferrer"
            class="transition-colors text-white/40 hover:text-cyan-400"
            title="Abrir link"
          >
            <ExternalLink :size="20" />
          </a>
          
          <button
            @click="btnDelete"
            class="transition-colo text-white/40 hover:text-red-400"
            title="Deletar link"
          >
            <Trash2 :size="20" />
          </button>
        </div>
      </div>

      <p class="text-sm leading-relaxed mb-6 line-clamp-3 font-medium text-gray-300">
        {{ link.description }}
      </p>
    </div>

    <div class="flex items-center justify-between mt-auto">
      <div class="flex flex-wrap gap-2">
        <span 
          v-for="tag in link.tags" 
          :key="tag"
          class="flex items-center text-[10px] uppercase tracking-wider 
                 font-semibold px-2.5 py-1 rounded-full border 
                 bg-white/5 border-white/5 text-gray-400"
        >
          <span class="mr-1 opacity-50">#</span>{{ tag }}
        </span>
      </div>
    </div>
  </div>
  <ConfirmCard
    :show="showConfirm"
    title="Deletar Link"
    :message="`Tem certeza que deseja deletar o link '${link.title}'?`"
    @confirm="confirmDelete"
    @cancel="cancelDelete"
  />
</template>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>