<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="min-h-screen bg-gray-100 p-8">
    <h1 class="text-2xl font-bold mb-4">Bienvenue, {{ authStore.nom }}</h1>

    <div class="space-x-4">
      <RouterLink to="/results" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
        Voir mes résultats
      </RouterLink>
      <RouterLink
        to="/profile"
        class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded"
      >
        Mon profil
      </RouterLink>
      <button @click="logout" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded">
        Déconnexion
      </button>
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
