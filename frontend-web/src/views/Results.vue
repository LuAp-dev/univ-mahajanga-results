<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="w-full min-h-full p-8 bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-100">
    <div class="max-w-7xl mx-auto">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
        <h2 class="text-2xl md:text-3xl font-bold">
          Mes Résultats — {{ student.nom }} {{ student.prenom }} ({{ student.matricule }})
        </h2>
        <RouterLink
          to="/dashboard"
          class="bg-gray-300 hover:bg-gray-400 dark:bg-gray-700 dark:hover:bg-gray-600 text-black dark:text-white px-4 py-2 rounded-lg transition-colors"
        >
          Retour au Dashboard
        </RouterLink>
      </div>

      <div class="mb-6">
        <input
          v-model="search"
          placeholder="Rechercher une matière..."
          class="p-3 border border-gray-300 dark:border-gray-600 rounded-lg w-full max-w-md dark:bg-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
      </div>

      <div v-if="loading" class="flex justify-center items-center h-32">
        <div class="text-lg">Chargement...</div>
      </div>

      <div
        v-else-if="error"
        class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 p-4 rounded-lg"
      >
        {{ error }}
      </div>

      <div v-else class="space-y-6">
        <div
          v-for="ue in filteredResults"
          :key="ue.ue_nom"
          class="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden"
        >
          <div
            class="bg-gray-50 dark:bg-gray-700 px-6 py-4 border-b border-gray-200 dark:border-gray-600"
          >
            <h3 class="text-xl font-semibold">
              UE : {{ ue.ue_nom }}
              <span class="text-sm font-normal text-gray-600 dark:text-gray-400"
                >(Crédit : {{ ue.ue_credit }})</span
              >
            </h3>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-gray-100 dark:bg-gray-700">
                <tr>
                  <th
                    class="px-6 py-3 text-left text-sm font-medium text-gray-700 dark:text-gray-300"
                  >
                    Matière
                  </th>
                  <th
                    class="px-6 py-3 text-center text-sm font-medium text-gray-700 dark:text-gray-300"
                  >
                    Note
                  </th>
                  <th
                    class="px-6 py-3 text-center text-sm font-medium text-gray-700 dark:text-gray-300"
                  >
                    Décision du jury
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200 dark:divide-gray-600">
                <tr
                  v-for="ec in ue.ecs"
                  :key="ec.ec_nom"
                  v-show="matchesSearch(ec.ec_nom)"
                  class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
                >
                  <td class="px-6 py-4 text-sm">{{ ec.ec_nom }}</td>
                  <td
                    class="px-6 py-4 text-sm text-center font-semibold"
                    :class="
                      ec.note >= 10
                        ? 'text-green-600 dark:text-green-400'
                        : 'text-red-600 dark:text-red-400'
                    "
                  >
                    {{ ec.note }}
                  </td>
                  <td class="px-6 py-4 text-sm text-center">
                    <span
                      class="px-2 py-1 rounded-full text-xs font-medium"
                      :class="
                        ec.decision === 'ADMIS'
                          ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300'
                          : 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300'
                      "
                    >
                      {{ ec.decision }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Moyenne en dehors de la boucle -->
        <div
          v-if="average !== null"
          class="text-right text-lg font-bold mt-6 border-t pt-4 border-gray-300 dark:border-gray-700"
        >
          Moyenne pondérée : {{ average }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const results = ref([])
const average = ref(null)
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
    average.value = response.data.average
    // eslint-disable-next-line no-unused-vars
  } catch (err) {
    error.value = 'Erreur lors du chargement des résultats.'
  } finally {
    loading.value = false
  }
})
</script>
