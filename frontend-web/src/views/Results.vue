<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="flex-grow p-8 bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-100">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">
        Mes Résultats — {{ student.nom }} {{ student.prenom }} ({{ student.matricule }})
      </h2>
      <RouterLink
        to="/dashboard"
        class="bg-gray-300 hover:bg-gray-400 dark:bg-gray-700 dark:hover:bg-gray-600 text-black dark:text-white px-4 py-2 rounded"
      >
        Retour au Dashboard
      </RouterLink>
    </div>

    <input
      v-model="search"
      placeholder="Rechercher une matière..."
      class="mb-6 p-2 border border-gray-300 dark:border-gray-600 rounded w-full max-w-md dark:bg-gray-800 dark:text-white"
    />

    <div v-if="loading">Chargement...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>
    <div v-else>
      <div v-for="ue in filteredResults" :key="ue.ue_nom" class="mb-6">
        <h3 class="text-xl font-semibold mb-2">
          UE : {{ ue.ue_nom }} (Crédit : {{ ue.ue_credit }})
        </h3>
        <table class="w-full border border-gray-300 dark:border-gray-600 mb-4">
          <thead class="bg-gray-200 dark:bg-gray-700">
            <tr>
              <th class="p-2">Matière</th>
              <th class="p-2">Note</th>
              <th class="p-2">Décision du jury</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="ec in ue.ecs"
              :key="ec.ec_nom"
              v-show="matchesSearch(ec.ec_nom)"
              class="text-center border-t border-gray-300 dark:border-gray-700"
            >
              <td class="p-2">{{ ec.ec_nom }}</td>
              <td class="p-2">{{ ec.note }}</td>
              <td class="p-2">{{ ec.decision }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const results = ref([])
const student = ref({})
const loading = ref(true)
const error = ref(null)
const search = ref('')
const authStore = useAuthStore()

const filteredResults = computed(() => {
  if (!search.value) return results.value
  return results.value.filter((ue) =>
    ue.ecs.some((ec) => ec.ec_nom.toLowerCase().includes(search.value.toLowerCase())),
  )
})

const matchesSearch = (ecNom) =>
  !search.value || ecNom.toLowerCase().includes(search.value.toLowerCase())

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
    student.value = me.data
    const id = me.data.id
    const response = await axios.get(`http://localhost:8000/api/v1/students/${id}/results`, config)
    results.value = response.data.results
    // eslint-disable-next-line no-unused-vars
  } catch (err) {
    error.value = 'Erreur lors du chargement des résultats.'
  } finally {
    loading.value = false
  }
})
</script>
