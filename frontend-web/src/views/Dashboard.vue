<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="w-full min-h-full bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-100 p-8">
    <div class="max-w-6xl mx-auto">
      <h1 class="text-3xl font-bold mb-6">Bienvenue, {{ authStore.nom }}</h1>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <RouterLink
          to="/results"
          class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-4 rounded-lg text-center transition-colors shadow-md"
        >
          <div class="text-lg font-semibold">Voir mes résultats</div>
          <div class="text-sm opacity-90 mt-1">Consulter mes notes et décisions</div>
        </RouterLink>
        <RouterLink
          to="/profile"
          class="bg-green-500 hover:bg-green-600 text-white px-6 py-4 rounded-lg text-center transition-colors shadow-md"
        >
          <div class="text-lg font-semibold">Mon profil</div>
          <div class="text-sm opacity-90 mt-1">Informations personnelles</div>
        </RouterLink>
        <button
          @click="logout"
          class="bg-red-500 hover:bg-red-600 text-white px-6 py-4 rounded-lg transition-colors shadow-md"
        >
          <div class="text-lg font-semibold">Déconnexion</div>
          <div class="text-sm opacity-90 mt-1">Quitter la session</div>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
