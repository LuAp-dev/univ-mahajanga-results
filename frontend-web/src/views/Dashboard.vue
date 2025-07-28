<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div
    class="w-full min-h-full bg-gray-900 text-gray-100 flex flex-col items-center justify-center p-8"
  >
    <div class="text-center">
      <h1 class="text-4xl font-bold mb-8">Bienvenue, {{ authStore.nom }}</h1>

      <div class="flex flex-col md:flex-row items-center justify-center gap-6">
        <RouterLink
          to="/results"
          class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg text-lg shadow transition-colors"
        >
          Voir mes résultats
        </RouterLink>

        <RouterLink
          to="/profile"
          class="bg-green-600 hover:bg-green-700 text-white px-8 py-4 rounded-lg text-lg shadow transition-colors"
        >
          Mon profil
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
</script>
