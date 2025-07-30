<template>
  <div>
    <button
      v-if="!isOpen"
      @click="toggleChat"
      class="fixed bottom-6 right-6 w-16 h-16 bg-gray-800 text-white rounded-full shadow-lg flex items-center justify-center hover:bg-gray-700 transition-colors"
    >
      🤖
    </button>

    <div
      v-else
      class="fixed bottom-6 right-6 w-80 h-[500px] bg-gray-900 text-white rounded-lg shadow-lg flex flex-col"
    >
      <div class="bg-gray-800 px-4 py-2 flex justify-between items-center rounded-t-lg">
        <h3 class="text-sm font-bold">Assistant Étudiant</h3>
        <button @click="closeChat" class="text-gray-400 hover:text-white">✖</button>
      </div>

      <div class="flex-1 overflow-y-auto px-4 py-2 space-y-2">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          class="flex items-start"
          :class="msg.sender === 'bot' ? 'justify-start' : 'justify-end'"
        >
          <img
            v-if="msg.sender === 'bot'"
            src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png"
            class="w-8 h-8 rounded-full mr-2"
            alt="bot"
          />
          <div
            class="inline-block px-4 py-2 rounded-lg text-sm whitespace-pre-line"
            :class="msg.sender === 'bot' ? 'bg-gray-700 text-left' : 'bg-blue-600 text-right'"
          >
            {{ msg.text }}
          </div>
          <img
            v-if="msg.sender === 'user'"
            src="https://cdn-icons-png.flaticon.com/512/9131/9131529.png"
            class="w-8 h-8 rounded-full ml-2"
            alt="user"
          />
        </div>
      </div>

      <div class="p-3 border-t border-gray-700">
        <form @submit.prevent="handleSend" class="flex gap-2">
          <input
            v-model="input"
            type="text"
            placeholder="Écris ici..."
            class="flex-1 p-2 rounded-lg bg-gray-800 text-white border border-gray-600 focus:outline-none"
          />
          <button
            type="submit"
            class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg text-white"
          >
            ➤
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const isOpen = ref(false)
const input = ref('')
const step = ref(0)
const matricule = ref('')
const student = ref(null)
const rawResults = ref([])
const messages = ref([{ sender: 'bot', text: 'Bienvenue ! Quel est ton matricule ?' }])

function toggleChat() {
  isOpen.value = true
}

function closeChat() {
  isOpen.value = false
  input.value = ''
  step.value = 0
  matricule.value = ''
  student.value = null
  rawResults.value = []
  messages.value = [{ sender: 'bot', text: 'Bienvenue ! Quel est ton matricule ?' }]
}

async function handleSend() {
  if (!input.value.trim()) return

  messages.value.push({ sender: 'user', text: input.value })
  const userInput = input.value.trim()
  input.value = ''
  const messageText = userInput.toLowerCase()

  if (step.value === 0) {
    try {
      const res = await axios.get(`http://localhost:8000/api/v1/chatbot/student/${userInput}`)
      student.value = res.data
      matricule.value = userInput
      step.value = 1
      messages.value.push({
        sender: 'bot',
        text: `Bonjour ${res.data.prenom} ! Veux-tu voir ton "profil" ou tes "résultats" ?`,
      })
      // eslint-disable-next-line no-unused-vars
    } catch (err) {
      messages.value.push({ sender: 'bot', text: 'Matricule introuvable. Réessaie.' })
    }
  } else if (step.value >= 1) {
    if (messageText.includes('profil')) {
      try {
        const res = await axios.get(
          `http://localhost:8000/api/v1/chatbot/student/${student.value.id}/profile`,
        )
        const s = res.data
        messages.value.push({
          sender: 'bot',
          text: `Nom : ${s.nom}\nPrénom : ${s.prenom}\nSexe : ${s.sexe}\nMatricule : ${s.matricule}\nNiveau : ${s.niveau ?? 'Non spécifié'}`,
        })
        step.value = 2
        messages.value.push({
          sender: 'bot',
          text: 'Tu peux taper "résultats" ou "fermer".',
        })
        // eslint-disable-next-line no-unused-vars
      } catch (e) {
        messages.value.push({ sender: 'bot', text: 'Erreur lors du chargement du profil.' })
      }
    } else if (messageText.includes('résultats')) {
      try {
        const res = await axios.get(
          `http://localhost:8000/api/v1/chatbot/student/${student.value.id}/results`,
        )
        rawResults.value = res.data.results

        for (const ue of rawResults.value) {
          let ueText = `UE : ${ue.ue_nom} (${ue.ue_credit} crédits)\n`
          for (const ec of ue.ecs) {
            ueText += `  - ${ec.ec_nom} : ${ec.note} (${ec.decision})\n`
          }
          messages.value.push({ sender: 'bot', text: ueText })
        }

        if (res.data.average !== null) {
          messages.value.push({
            sender: 'bot',
            text: `Moyenne pondérée : ${res.data.average}`,
          })
        }

        step.value = 2
        messages.value.push({
          sender: 'bot',
          text: 'Tu peux taper "profil" ou "fermer".',
        })
        // eslint-disable-next-line no-unused-vars
      } catch (e) {
        messages.value.push({ sender: 'bot', text: 'Erreur lors du chargement des résultats.' })
      }
    }
  } else if (messageText.includes('fermer')) {
    closeChat()
  } else {
    messages.value.push({
      sender: 'bot',
      text: 'Tu peux taper "profil", "résultats" ou "fermer".',
    })
  }
}
</script>
