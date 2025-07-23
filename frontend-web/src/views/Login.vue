<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="bg-white p-8 rounded shadow-md w-full max-w-md">
      <h2 class="text-2xl font-bold mb-6 text-center">Connexion Étudiant</h2>

      <form @submit.prevent="login" class="space-y-4">
        <div>
          <label for="matricule" class="block text-sm font-medium text-gray-700">Matricule</label>
          <input
            v-model="matricule"
            type="text"
            id="matricule"
            required
            class="mt-1 block w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
            placeholder="Entrez votre matricule"
          />
        </div>

        <button
          type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded"
        >
          Se connecter
        </button>

        <p v-if="error" class="text-red-500 text-sm text-center">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const matricule = ref('')
const error = ref(null)
const router = useRouter()
const authStore = useAuthStore()

const login = async () => {
  error.value = null
  try {
    await authStore.login(matricule.value)
    router.push('/dashboard')
    // eslint-disable-next-line no-unused-vars
  } catch (err) {
    error.value = 'Connexion échouée. Vérifie ton matricule.'
  }
}
</script>
