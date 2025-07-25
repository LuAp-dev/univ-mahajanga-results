<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="min-h-screen bg-white p-8">
    <h2 class="text-2xl font-bold mb-6">Mon Profil</h2>

    <div v-if="loading">Chargement...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>
    <div v-else class="max-w-lg">
      <table class="w-full table-auto border border-gray-200 shadow-md rounded">
        <tbody>
          <tr class="border-b">
            <td class="font-semibold px-4 py-2">Nom</td>
            <td class="px-4 py-2">{{ form.nom }}</td>
          </tr>
          <tr class="border-b">
            <td class="font-semibold px-4 py-2">Prénom</td>
            <td class="px-4 py-2">{{ form.prenom }}</td>
          </tr>
          <tr class="border-b">
            <td class="font-semibold px-4 py-2">Sexe</td>
            <td class="px-4 py-2">{{ form.sexe === 'M' ? 'Masculin' : 'Féminin' }}</td>
          </tr>
          <tr class="border-b">
            <td class="font-semibold px-4 py-2">Matricule</td>
            <td class="px-4 py-2">{{ form.matricule }}</td>
          </tr>
          <tr>
            <td class="font-semibold px-4 py-2">Niveau</td>
            <td class="px-4 py-2">{{ form.niveau }}</td>
          </tr>
        </tbody>
      </table>

      <RouterLink
        to="/dashboard"
        class="inline-block mt-6 bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
      >
        Retour au Dashboard
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const loading = ref(true)
const error = ref(null)
const authStore = useAuthStore()
// eslint-disable-next-line no-unused-vars
const router = useRouter()

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
  } catch (err) {
    console.error(err)
    error.value = 'Erreur lors du chargement du profil.'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
td {
  border: 1px solid #e5e7eb;
}
</style>
