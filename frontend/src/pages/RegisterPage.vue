<script setup lang="ts">
import { ref } from 'vue';
import { useRouter, RouterLink } from 'vue-router';
import { UserPlus, Loader2 } from 'lucide-vue-next';
import { registerUser } from '../services/authService';
import Alert from '../components/Alert.vue';

const router = useRouter();

const formData = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
});

const error = ref('');
const showError = ref(false);
const isLoading = ref(false);

const registerSubmit = async () => {
  error.value = '';
  showError.value = false;

  if (formData.value.password !== formData.value.confirmPassword) {
    error.value = 'As senhas não coincidem.';
    showError.value = true;
    return;
  }

  if (formData.value.password.length < 6) {
    error.value = 'A senha deve ter pelo menos 6 caracteres.';
    showError.value = true;
    return;
  }

  isLoading.value = true;

  try {
    const result = await registerUser(
      formData.value.username, 
      formData.value.email, 
      formData.value.password
    );
    
    if (result.success) {
      router.push('/');
    } else {
      error.value = result.message;
      showError.value = true;
    }
  } catch (err: any) {
    error.value = err.message || 'Erro ao criar conta. Tente novamente.';
    showError.value = true;
  } finally {
    isLoading.value = false; 
  }
};
</script>

<template>
  <div class="flex items-center justify-center min-h-screen p-4">
    <div class="w-full max-w-md">
      <div 
        class="relative rounded-3xl border p-8 shadow-2xl backdrop-blur-xl transition-all
               bg-slate-900/60 border-white/10 text-white"
      >
        <div class="mb-8 text-center">
          <div 
            class="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full 
                    bg-purple-500/20 text-purple-400"
          >
            <UserPlus :size="28" />
          </div>
          <h1 class="text-2xl font-bold">Crie sua Conta</h1>
          <p class="mt-2 text-sm text-slate-400">
            Junte-se à comunidade LibraryLinks.
          </p>
        </div>

        <form @submit.prevent="registerSubmit" class="space-y-4">
          <Alert 
            :show="showError"
            type="error"
            :message="error"
            @dismiss="showError = false"
            class="mb-4"
          />

          <div>
            <label class="mb-1 block text-sm font-medium">
              Nome de Usuário
            </label>
            <input
              v-model="formData.username"
              required
              type="text"
              :disabled="isLoading"
              class="w-full rounded-xl border px-4 py-3 
                     outline-hidden focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 
                     border-white/10 bg-black/20 text-white transition-all
                     disabled:opacity-50 disabled:cursor-not-allowed"
              placeholder="Como quer ser chamado?"
            />
          </div>

          <div>
            <label class="mb-1 block text-sm font-medium">
              Email
            </label>
            <input
              v-model="formData.email"
              required
              type="email"
              :disabled="isLoading"
              class="w-full rounded-xl border  px-4 py-3 
                     outline-hidden focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 
                     border-white/10 bg-black/20 text-white transition-all
                     disabled:opacity-50 disabled:cursor-not-allowed"
              placeholder="seu@email.com"
            />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="mb-1 block text-sm font-medium">
                Senha
              </label>
              <input
                v-model="formData.password"
                required
                type="password"
                :disabled="isLoading"
                class="w-full rounded-xl border px-4 py-3 
                       outline-hidden focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 
                       border-white/10 bg-black/20 text-white transition-all
                       disabled:opacity-50 disabled:cursor-not-allowed"
                placeholder="••••••••"
              />
            </div>
            <div>
              <label class="mb-1 block text-sm font-medium">
                Confirmar Senha
              </label>
              <input
                v-model="formData.confirmPassword"
                required
                type="password"
                :disabled="isLoading"
                class="w-full rounded-xl border px-4 py-3 
                       outline-hidden focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 
                       border-white/10 bg-black/20 text-white transition-all
                       disabled:opacity-50 disabled:cursor-not-allowed"
                placeholder="••••••••"
              />
            </div>
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full mt-2 rounded-xl bg-purple-600 py-3.5 font-bold text-white 
                   shadow-lg shadow-purple-500/25 transition-all 
                   hover:shadow-purple-500/40 hover:-translate-y-0.5 active:scale-95
                   disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none
                   flex items-center justify-center gap-2"
          >
            <template v-if="isLoading">
              <Loader2 :size="20" class="animate-spin" />
              Criando conta...
            </template>
            <template v-else>
              Criar Conta
            </template>
          </button>
        </form>

        <div class="mt-8 text-center text-sm">
          <span class="text-slate-400">Já tem uma conta? </span>
          <RouterLink 
            to="/login" 
            class="font-semibold text-purple-400 hover:text-purple-500 hover:underline"
          >
            Entrar
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>