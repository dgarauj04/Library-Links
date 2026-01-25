<script setup lang="ts">
import { MessageSquare, Instagram, Linkedin, Github, Link as LinkIcon } from 'lucide-vue-next';

const emit = defineEmits<{
  (e: 'openFeedback'): void
}>();

const socialLinks = [
  { label: 'Instagram', href: 'https://instagram.com/dgaraujoo_', icon: Instagram, color: 'pink-800/80', color_hover: 'pink-600' },
  { label: 'LinkedIn', href: 'https://www.linkedin.com/in/douglas-araujo-dgprogdev', icon: Linkedin, color: 'sky-800/85', color_hover: 'sky-600' },
  { label: 'GitHub', href: 'https://github.com/dgarauj04', icon: Github, color: 'purple-800/80', color_hover: 'purple-600' },
  { label: 'Portfólio', href: 'https://daraujodb-dev.vercel.app/', icon: LinkIcon, color: 'amber-800/80', color_hover: 'amber-600' },
];
</script>

<template>
  <footer class="w-full py-6 px-4 bg-transparent backdrop-blur-sm border-t border-gray-200/20 mt-20">
    <div class="max-w-6xl mx-auto flex flex-col items-center justify-between gap-6">
      
      <div class="flex-1">
        <button
          class="flex items-center gap-2 px-6 py-2.5 bg-emerald-700/50 hover:bg-emerald-600/85 text-white font-medium rounded-full transition-all active:scale-95 shadow-sm"
          @click="emit('openFeedback')"
        >
          <MessageSquare :size="20" />
          <span>Enviar Feedback</span>
        </button>
      </div>

      <div class="flex flex-wrap justify-center items-center gap-6">
        <a v-for="link in socialLinks" 
           :key="link.label"
           :href="link.href"
           target="_blank"
           rel="noopener noreferrer"
           :class="`text-${link.color} hover:text-${link.color_hover} transition-colors`" 
           class="group flex items-center gap-2 font-medium  hover:link.color-hover transition-colors"
           :aria-label="link.label"
        >
          <component :is="link.icon" :size="20" class="group-hover:scale-110 transition-transform" />
          <span class="hidden sm:inline">{{ link.label }}</span>
        </a>
      </div>

    </div>

    <div class="mt-8 pt-6 border-t border-gray-100/20 text-center">
      <p class="text-xs text-gray-400">
        © {{ new Date().getFullYear() }} — Desenvolvido com carinho por Douglas Araujo.
      </p>
    </div>
  </footer>
</template>