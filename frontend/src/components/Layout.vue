<script setup lang="ts">
</script>

<template>
  <div 
    class="min-h-screen relative overflow-hidden font-sans transition-colors duration-500 
           bg-[#0f172a] text-slate-300 selection:bg-cyan-500/30 selection:text-cyan-100"
  >
    <div class="fixed inset-0 z-0 overflow-hidden pointer-events-none">
      <div class="absolute top-0 -left-4 w-96 h-96 rounded-full mix-blend-multiply filter blur-[100px] opacity-40 animate-blob transition-colors duration-500 bg-purple-300 dark:bg-purple-600"></div>
      <div class="absolute top-0 -right-4 w-96 h-96 rounded-full mix-blend-multiply filter blur-[100px] opacity-40 animate-blob animation-delay-2000 transition-colors duration-500 bg-cyan-300 dark:bg-cyan-600"></div>
      <div class="absolute -bottom-8 left-20 w-96 h-96 rounded-full mix-blend-multiply filter blur-[100px] opacity-40 animate-blob animation-delay-4000 transition-colors duration-500 bg-pink-300 dark:bg-pink-600"></div>
      <div class="absolute inset-0 bg-[url('https://grainy-linears.vercel.app/noise.svg')] opacity-20 brightness-100 contrast-150 mix-blend-overlay"></div>
    </div>

    <main class="relative z-10 py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
@keyframes blob {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
}
.animate-blob { animation: blob 7s infinite; }
.animation-delay-2000 { animation-delay: 2s; }
.animation-delay-4000 { animation-delay: 4s; }
</style>