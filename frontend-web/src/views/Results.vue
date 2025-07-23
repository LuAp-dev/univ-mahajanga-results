<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="min-h-screen p-8 bg-white">
    <h2 class="text-2xl font-bold mb-4">Mes Résultats</h2>

    <div v-if="loading">Chargement...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>
    <div v-else>
      <table class="w-full border border-gray-300">
        <thead class="bg-gray-200">
          <tr>
            <th class="p-2">Matière</th>
            <th class="p-2">Note</th>
            <th class="p-2">Crédit</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="res in results" :key="res.id" class="text-center">
            <td class="p-2">{{ res.ec_nom }}</td>
            <td class="p-2">{{ res.note }}</td>
            <td class="p-2">{{ res.decision }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const results = ref([])
const loading = ref(true)
const error = ref(null)
const authStore = useAuthStore()

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    error.value = 'Non connecté.'
    loading.value = false
    return
  }

  try {
    const config = {
      headers: { Authorization: `Bearer ${authStore.accessToken}` },
    }
    const me = await axios.get('http://localhost:8000/api/v1/students/me', config)
    const id = me.data.id
    const response = await axios.get(`http://localhost:8000/api/v1/students/${id}/results`, config)
    console.log(response.data)
    results.value = response.data.results
    // eslint-disable-next-line no-unused-vars
  } catch (e) {
    error.value = 'Erreur de chargement des résultats'
  } finally {
    loading.value = false
  }
})
</script>
