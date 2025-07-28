<script setup>
import { RouterView } from 'vue-router'
import { ref, watchEffect } from 'vue'

const darkMode = ref(false)

watchEffect(() => {
  document.documentElement.classList.toggle('dark', darkMode.value)
})
</script>

<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-100">
    <header class="flex items-center justify-between p-4">
      <img
        src="https://www.mahajanga-univ.mg/storage/settings/ET2YH6R099vUaVEXRhymS3etHDZngsWy4YcWGKKM.png"
        alt="Logo Université Mahajanga"
        class="h-12"
      />
      <button
        class="bg-gray-300 dark:bg-gray-700 text-sm text-black dark:text-white px-3 py-1 rounded hover:bg-gray-400 dark:hover:bg-gray-600"
        @click="darkMode = !darkMode"
      >
        {{ darkMode ? 'Mode Clair' : 'Mode Sombre' }}
      </button>
    </header>

    <main class="min-h-[calc(100vh-64px)] flex flex-col">
      <router-view />
    </main>
  </div>
</template>
