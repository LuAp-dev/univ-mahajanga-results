<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="w-full min-h-full flex items-center justify-center bg-gray-100 dark:bg-gray-900 p-4">
    <div class="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-lg w-full max-w-md">
      <h2 class="text-2xl font-bold mb-6 text-center text-gray-900 dark:text-gray-100">
        Connexion Étudiant
      </h2>
      <form @submit.prevent="login" class="space-y-4">
        <div>
          <label
            for="matricule"
            class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            Matricule
          </label>
          <input
            v-model="matricule"
            type="text"
            id="matricule"
            required
            class="w-full border border-gray-300 dark:border-gray-600 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 dark:bg-gray-700 dark:text-white transition-colors"
            placeholder="Entrez votre matricule"
          />
        </div>

        <div>
          <label
            for="password"
            class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            Mot de passe
          </label>
          <input
            v-model="password"
            type="password"
            id="password"
            required
            class="w-full border border-gray-300 dark:border-gray-600 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 dark:bg-gray-700 dark:text-white transition-colors"
            placeholder="Entrez votre mot de passe"
          />
        </div>

        <button
          type="submit"
          :disabled="!matricule.trim() || !password.trim()"
          class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white py-3 px-4 rounded-lg transition-colors"
        >
          Se connecter
        </button>

        <p
          v-if="error"
          class="text-red-500 text-sm text-center bg-red-50 dark:bg-red-900/20 p-2 rounded"
        >
          {{ error }}
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const matricule = ref('')
const password = ref('')
const error = ref(null)
const router = useRouter()
const authStore = useAuthStore()

const login = async () => {
  error.value = null
  try {
    await authStore.login(matricule.value, password.value)
    router.push('/dashboard')
    // eslint-disable-next-line no-unused-vars
  } catch (err) {
    error.value = 'Connexion échouée. Vérifie ton matricule et ton mot de passe.'
  }
}
</script>
