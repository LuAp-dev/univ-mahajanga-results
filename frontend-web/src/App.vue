<script setup>
import { RouterView, useRoute, useRouter } from 'vue-router'
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import ChatBot from '@/components/ChatBot.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// On cache le bouton sur la page login
const showLogout = computed(() => route.path !== '/login')

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="dark min-h-screen flex flex-col w-full bg-gray-900 text-gray-100">
    <header
      class="w-full flex items-center justify-between px-6 py-4 border-b border-gray-700 bg-gray-800 shadow"
    >
      <!-- Logo Université à gauche -->
      <img
        src="https://www.mahajanga-univ.mg/storage/settings/ET2YH6R099vUaVEXRhymS3etHDZngsWy4YcWGKKM.png"
        alt="Logo Université Mahajanga"
        class="h-12 object-contain"
      />

      <!-- Titre centré -->
      <h1 class="text-lg font-semibold text-center text-white flex-1">
        Faculté de Médecine – Consultation des résultats
      </h1>

      <!-- Logo Faculté à droite + bouton logout -->
      <div class="flex items-center space-x-4">
        <img
          src="https://www.mahajanga-univ.mg/storage/etabs/kJyFlHJbjW8dQS3Z7A04u4pACX4bWmD3LKaT92kH.png"
          alt="Logo Faculté de Médecine"
          class="h-12 object-contain"
        />
        <button
          v-if="showLogout"
          @click="logout"
          class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded transition-colors"
        >
          Déconnexion
        </button>
      </div>
    </header>

    <main class="flex-1 w-full min-h-[calc(100vh-80px)] pb-16">
      <RouterView />
    </main>

    <!-- Footer global -->
    <footer
      class="fixed bottom-0 left-0 w-full text-left text-gray-500 text-sm px-6 py-2 bg-gray-900 z-40"
    >
      Copyrights © 2025 Université de Mahajanga | DTIC
    </footer>

    <!-- ChatBot -->
    <ChatBot />
  </div>
</template>

<style>
html,
body,
#app {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}
</style>
