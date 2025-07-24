<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="min-h-screen bg-white p-8">
    <h2 class="text-2xl font-bold mb-4">Mon Profil</h2>

    <div v-if="loading">Chargement...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>
    <div v-else>
      <form @submit.prevent="updateProfile" class="space-y-4 max-w-md">
        <div>
          <label class="block mb-1 font-semibold">Nom</label>
          <input v-model="form.nom" type="text" class="w-full border border-gray-300 p-2 rounded" />
        </div>

        <div>
          <label class="block mb-1 font-semibold">Prénom</label>
          <input
            v-model="form.prenom"
            type="text"
            class="w-full border border-gray-300 p-2 rounded"
          />
        </div>

        <div>
          <label class="block mb-1 font-semibold">Sexe</label>
          <select v-model="form.sexe" class="w-full border border-gray-300 p-2 rounded">
            <option value="M">Masculin</option>
            <option value="F">Féminin</option>
          </select>
        </div>

        <div>
          <label class="block mb-1 font-semibold">Matricule</label>
          <input
            v-model="form.matricule"
            type="text"
            class="w-full border border-gray-300 p-2 rounded bg-gray-100"
            disabled
          />
        </div>

        <div>
          <label class="block mb-1 font-semibold">Niveau</label>
          <input
            :value="form.niveau"
            type="text"
            class="w-full border border-gray-300 p-2 rounded bg-gray-100"
            disabled
          />
        </div>

        <button type="submit" class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
          Enregistrer
        </button>

        <RouterLink
          to="/dashboard"
          class="inline-block ml-4 bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
        >
          Retour au Dashboard
        </RouterLink>
      </form>
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
    // eslint-disable-next-line no-unused-vars
  } catch (err) {
    error.value = 'Erreur lors du chargement du profil.'
  } finally {
    loading.value = false
  }
})

const updateProfile = async () => {
  try {
    const config = {
      headers: { Authorization: `Bearer ${authStore.accessToken}` },
    }
    await axios.put(
      `http://localhost:8000/api/v1/students/${authStore.user.id}`,
      {
        nom: form.value.nom,
        prenom: form.value.prenom,
        sexe: form.value.sexe,
      },
      config,
    )
    alert('Profil mis à jour avec succès.')
    // eslint-disable-next-line no-unused-vars
  } catch (err) {
    alert('Erreur lors de la mise à jour du profil.')
  }
}
</script>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 40px auto;
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h1 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.profile-picture img {
  width: 120px;
  height: 120px;
  border-radius: 100px;
  border: 2px solid #ccc;
  margin-bottom: 20px;
}

.profile-card {
  margin-top: 10px;
  text-align: left;
}

.profile-row {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px solid #eee;
}

.label {
  font-weight: bold;
  color: #444;
}

.value {
  color: #222;
}

.profile-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.btn {
  padding: 8px 16px;
  font-weight: bold;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
}

.return {
  background-color: #3182ce;
  color: white;
}

.edit {
  background-color: #38a169;
  color: white;
}
</style>
