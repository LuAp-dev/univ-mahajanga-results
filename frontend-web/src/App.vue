<script setup>
import { RouterView } from 'vue-router'
import { ref, watchEffect, onMounted } from 'vue'

const darkMode = ref(false)

// Initialiser le mode selon la préférence système ou localStorage
onMounted(() => {
  const savedMode = localStorage.getItem('darkMode')
  if (savedMode !== null) {
    darkMode.value = savedMode === 'true'
  } else {
    // Utiliser la préférence système par défaut
    darkMode.value = window.matchMedia('(prefers-color-scheme: dark)').matches
  }
})

watchEffect(() => {
  document.documentElement.classList.toggle('dark', darkMode.value)
  localStorage.setItem('darkMode', darkMode.value.toString())
})

const toggleDarkMode = () => {
  darkMode.value = !darkMode.value
}
</script>

<template>
  <div class="min-h-screen w-full bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-100">
    <header
      class="w-full flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700"
    >
      <img
        src="https://www.mahajanga-univ.mg/storage/settings/ET2YH6R099vUaVEXRhymS3etHDZngsWy4YcWGKKM.png"
        alt="Logo Université Mahajanga"
        class="h-12"
      />
      <button
        class="bg-gray-300 dark:bg-gray-700 text-sm text-black dark:text-white px-3 py-1 rounded hover:bg-gray-400 dark:hover:bg-gray-600 transition-colors"
        @click="toggleDarkMode"
      >
        {{ darkMode ? 'Mode Clair' : 'Mode Sombre' }}
      </button>
    </header>

    <main class="w-full min-h-[calc(100vh-80px)]">
      <router-view />
    </main>
  </div>
</template>
