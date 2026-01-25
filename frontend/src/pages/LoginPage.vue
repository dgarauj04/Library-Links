<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRouter, RouterLink } from 'vue-router';
import { LogIn, Loader2 } from 'lucide-vue-next';
import { loginUser } from '../services/authService';
import Footer from '../components/Footer.vue';

const router = useRouter();

const identifier = ref('');
const password = ref('');
const error = ref('');
const isLoading = ref(false);
const isLoginSuccessful = ref(false);

const loginSubmit = async () => {
  error.value = '';
  isLoading.value = true;

  try {
    const result = await loginUser(identifier.value, password.value);
    
    if (result.success) {
      isLoginSuccessful.value = true;
    } else {
      error.value = result.message;
    }
  } catch (err: any) {
    error.value = err.message || 'Erro ao fazer login. Tente novamente.';
  } finally {
    isLoading.value = false;
  }
};

watch(isLoginSuccessful, (success) => {
  if (success) {
    router.replace('/');
  }
});
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-5 min-h-screen p-4">
    <div class="w-full max-w-md">
      <div 
        class="relative rounded-3xl border p-8 shadow-2xl backdrop-blur-xl transition-all
               bg-white/80 border-white/50 text-slate-900
               dark:bg-slate-900/60 dark:border-white/10 dark:text-white"
      >
        <div class="mb-8 text-center">
          <div 
            class="mx-auto mb-4 flex h-14 w-14 items-center justify-center 
                   rounded-full bg-cyan-500/10 text-cyan-600 
                   dark:bg-cyan-500/20 dark:text-cyan-400"
          >
            <LogIn :size="28" />
          </div>
          <h1 class="text-2xl font-bold">Bem-vindo de volta</h1>
          <p class="mt-2 text-sm text-slate-500 dark:text-slate-400">
            Entre para gerenciar seus links e contribuir.
          </p>
        </div>

        <form @submit.prevent="loginSubmit" class="space-y-5">
          <div 
            v-if="error" 
            class="p-3 text-sm rounded-lg bg-red-500/10 border border-red-500/20 
                   text-red-600 dark:text-red-400 text-center"
          >
            {{ error }}
          </div>

          <div>
            <label class="mb-1.5 block text-sm font-medium">
              Email ou Usuário
            </label>
            <input
              v-model="identifier"
              required
              type="text"
              :disabled="isLoading"
              class="w-full rounded-xl border border-slate-200 bg-white/50 px-4 py-3 
                     outline-hidden focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 
                     dark:border-white/10 dark:bg-black/20 dark:text-white transition-all 
                     disabled:opacity-50 disabled:cursor-not-allowed"
              placeholder="seunome ou email@exemplo.com"
            />
          </div>

          <div>
            <label class="mb-1.5 block text-sm font-medium">
              Senha
            </label>
            <input
              v-model="password"
              required
              type="password"
              :disabled="isLoading"
              class="w-full rounded-xl border border-slate-200 bg-white/50 px-4 py-3 
                     outline-hidden focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 
                     dark:border-white/10 dark:bg-black/20 dark:text-white transition-all 
                     disabled:opacity-50 disabled:cursor-not-allowed"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full rounded-xl bg-blue-500 py-3.5 
                   font-bold text-white shadow-lg shadow-cyan-500/25 transition-all 
                   hover:shadow-cyan-500/40 hover:-translate-y-0.5 active:scale-95 
                   disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none 
                   flex items-center justify-center gap-2"
          >
            <template v-if="isLoading">
              <Loader2 :size="20" class="animate-spin" />
              Entrando...
            </template>
            <template v-else>
              Entrar
            </template>
          </button>
        </form>

        <div class="mt-8 text-center text-sm">
          <span class="text-slate-500 dark:text-slate-400">Não tem uma conta? </span>
          <RouterLink 
            to="/register" 
            class="font-semibold text-cyan-400 hover:text-cyan-500 hover:underline"
          >
            Crie agora
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>