<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="w-full min-h-full bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-100 p-8">
    <div class="max-w-4xl mx-auto">
      <h2 class="text-3xl font-bold mb-6">Mon Profil</h2>

      <div v-if="loading" class="flex justify-center items-center h-32">
        <div class="text-lg">Chargement...</div>
      </div>

      <div
        v-else-if="error"
        class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 p-4 rounded-lg"
      >
        {{ error }}
      </div>

      <div v-else class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <table class="w-full">
          <tbody>
            <tr class="border-b border-gray-200 dark:border-gray-700">
              <td class="font-semibold px-4 py-4 text-gray-600 dark:text-gray-400 w-1/3">Nom</td>
              <td class="px-4 py-4">{{ form.nom }}</td>
            </tr>
            <tr class="border-b border-gray-200 dark:border-gray-700">
              <td class="font-semibold px-4 py-4 text-gray-600 dark:text-gray-400">Prénom</td>
              <td class="px-4 py-4">{{ form.prenom }}</td>
            </tr>
            <tr class="border-b border-gray-200 dark:border-gray-700">
              <td class="font-semibold px-4 py-4 text-gray-600 dark:text-gray-400">Sexe</td>
              <td class="px-4 py-4">{{ form.sexe === 'M' ? 'Masculin' : 'Féminin' }}</td>
            </tr>
            <tr class="border-b border-gray-200 dark:border-gray-700">
              <td class="font-semibold px-4 py-4 text-gray-600 dark:text-gray-400">Matricule</td>
              <td class="px-4 py-4 font-mono">{{ form.matricule }}</td>
            </tr>
            <tr>
              <td class="font-semibold px-4 py-4 text-gray-600 dark:text-gray-400">Niveau</td>
              <td class="px-4 py-4">{{ form.niveau }}</td>
            </tr>
          </tbody>
        </table>

        <div class="mt-6">
          <RouterLink
            to="/dashboard"
            class="inline-block bg-gray-500 hover:bg-gray-600 text-white px-6 py-3 rounded-lg transition-colors"
          >
            Retour au Dashboard
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const loading = ref(true)
const error = ref(null)
const authStore = useAuthStore()
const form = ref({
  nom: '',
  prenom: '',
  sexe: '',
  matricule: '',
  niveau: '',
})

onMounted(async () => {
  try {
    const config = {
      headers: { Authorization: `Bearer ${authStore.accessToken}` },
    }
    const res = await axios.get('http://localhost:8000/api/v1/students/me', config)
    Object.assign(form.value, res.data)
    authStore.user = res.data
    // eslint-disable-next-line no-unused-vars
  } catch (err) {
    error.value = 'Erreur lors du chargement du profil.'
  } finally {
    loading.value = false
  }
})
</script>
