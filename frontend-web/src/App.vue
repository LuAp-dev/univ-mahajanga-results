<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="min-h-screen bg-gray-50 text-gray-800">
    <router-view />
  </div>
</template>

<style>
/* Si tu n’utilises pas main.css ailleurs */
@import './assets/main.css';
</style>
