<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, watch } from 'vue';
import { X, Send, Loader, CheckCircle, AlertTriangle } from 'lucide-vue-next';
import emailjs from '@emailjs/browser';

const props = defineProps<{
  isOpen: boolean;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
}>();

type SubmissionStatus = 'idle' | 'sending' | 'success' | 'error';

const formData = reactive({
  name: '',
  email: '',
  message: ''
});

const status = ref<SubmissionStatus>('idle');
const feedbackMessage = ref('');

const serviceID = import.meta.env.VITE_EMAILJS_SERVICE_ID;
const templateID = import.meta.env.VITE_EMAILJS_TEMPLATE_ID;
const publicKey = import.meta.env.VITE_EMAILJS_PUBLIC_KEY;

watch(() => props.isOpen, (newValue) => {
  if (newValue) {
    status.value = 'idle';
    feedbackMessage.value = '';
  }
});


const clickClose = () => {
  if (status.value === 'sending') return;
  emit('close');
};

const clickEsc = (event: KeyboardEvent) => {
  if (event.key === 'Escape') {
    clickClose();
  }
};

const clickSubmit = async () => {
  status.value = 'sending';
  feedbackMessage.value = '';

  if (!serviceID || !templateID || !publicKey) {
    status.value = 'error';
    feedbackMessage.value = 'Erro de configuração. O administrador não configurou o serviço de email.';
    return;
  }

  const templateParams = {
    from_name: formData.name,
    from_email: formData.email,
    from_assunto: 'Feedback do Library Links',
    message: formData.message,
    date: new Date().toLocaleDateString('pt-BR'),
    year: new Date().getFullYear(),
  };

  try {
    await emailjs.send(serviceID, templateID, templateParams);
    
    status.value = 'success';
    feedbackMessage.value = 'Obrigado pelo seu feedback!';
    
    formData.name = '';
    formData.email = '';
    formData.message = '';
  } catch (err) {
    status.value = 'error';
    feedbackMessage.value = 'Falha ao enviar. Tente novamente mais tarde.';
    console.error('EmailJS Error:', err);
  }
};

onMounted(() => {
  if (publicKey) {
    emailjs.init(publicKey);
  }
  window.addEventListener('keydown', clickEsc);
});

onUnmounted(() => {
  window.removeEventListener('keydown', clickEsc);
});
</script>

<template>
  <Transition name="fade">
    <div 
      v-if="isOpen"
      class="fixed inset-0 -top-8 bg-black/60 backdrop-blur-sm w-full h-screen flex items-center justify-center z-50"
      @click.self="clickClose"
      aria-modal="true"
      role="dialog"
    >
      <div 
        class="bg-slate-800 rounded-xl p-6 border border-slate-700 max-w-xl w-full mx-4 relative shadow-2xl"
      >
        <button 
          @click="clickClose" 
          class="absolute top-3 right-3 text-slate-500 hover:text-white transition-colors"
          aria-label="Fechar modal"
        >
          <X :size="20" />
        </button>

        <h2 class="text-xl font-bold text-white mb-1">Envie seu Feedback</h2>
        <p class="text-sm text-slate-400 mb-6">
          Gostaria muito de ouvir suas sugestões e feedback sobre o Library Links!
        </p>
        
        <div v-if="status === 'success' || status === 'error'" class="text-center py-8">
          <CheckCircle v-if="status === 'success'" class="w-16 h-16 mx-auto text-green-500 mb-4" />
          <AlertTriangle v-else class="w-16 h-16 mx-auto text-red-500 mb-4" />
          
          <p :class="['text-lg font-semibold', status === 'success' ? 'text-green-400' : 'text-red-400']">
            {{ feedbackMessage }}
          </p>
          
          <button
            @click="clickClose"
            class="mt-6 px-4 py-2 text-sm font-semibold text-white bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors"
          >
            Fechar
          </button>
        </div>

        <form v-else @submit.prevent="clickSubmit" class="space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label for="name" class="block text-sm font-medium text-slate-300 mb-1">Nome</label>
              <input 
                v-model="formData.name"
                type="text" 
                id="name" 
                required 
                class="w-full bg-slate-900/80 border border-slate-600 rounded-lg p-2.5 text-sm text-slate-300 focus:ring-2 focus:ring-cyan-500 outline-none" 
              />
            </div>
            <div>
              <label for="email" class="block text-sm font-medium text-slate-300 mb-1">Email</label>
              <input 
                v-model="formData.email"
                type="email" 
                id="email" 
                required 
                class="w-full bg-slate-900/80 border border-slate-600 rounded-lg p-2.5 text-sm text-slate-300 focus:ring-2 focus:ring-cyan-500 outline-none" 
              />
            </div>
          </div>

          <div>
            <label for="message" class="block text-sm font-medium text-slate-300 mb-1">Sua Mensagem</label>
            <textarea 
              v-model="formData.message"
              id="message" 
              required 
              rows="4" 
              class="w-full bg-slate-900/80 border border-slate-600 rounded-lg p-2.5 text-sm text-slate-300 focus:ring-2 focus:ring-cyan-500 outline-none"
            ></textarea>
          </div>

          <button 
            type="submit" 
            :disabled="status === 'sending'"
            class="w-full flex items-center justify-center gap-2 bg-pink-800/45 text-white font-bold py-2.5 px-4 rounded-lg shadow-lg hover:bg-pink-700 hover:shadow-xl transform hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:cursor-wait"
          >
            <template v-if="status === 'sending'">
              <Loader class="w-5 h-5 animate-spin" />
              Enviando...
            </template>
            <template v-else>
              <Send class="w-5 h-5" />
              Enviar Feedback
            </template>
          </button>
        </form>
      </div>
    </div>
  </Transition>
</template>


<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>