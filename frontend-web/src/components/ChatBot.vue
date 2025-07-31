<template>
  <div>
    <!-- BOUTON DU CHATBOT AVANT OUVERTURE -->
    <button
      v-if="!isOpen"
      @click="toggleChat"
      class="fixed w-16 h-16 rounded-full shadow-lg flex items-center justify-center transition-colors z-50 chatbot-button"
      :class="{ 'chatbot-pulse': showPulse }"
    >
      <span class="relative z-10 text-white text-sm font-bold">
        🤖<br />
        <span v-if="showPulse" class="text-[10px]">Appuie ici !</span>
      </span>
      <span class="absolute w-full h-full rounded-full border-4 border-orange-600"></span>
    </button>

    <!-- FENÊTRE DU CHATBOT -->
    <div
      v-else
      class="fixed bottom-6 right-6 w-80 h-[500px] bg-gray-900 text-white rounded-lg shadow-lg flex flex-col z-50"
    >
      <div class="bg-gray-800 px-4 py-2 flex justify-between items-center rounded-t-lg">
        <h3 class="text-sm font-bold">Assistant Étudiant</h3>
        <button @click="closeChat" class="text-gray-400 hover:text-white">✖</button>
      </div>

      <transition-group name="chat" tag="div" class="flex-1 overflow-y-auto px-4 py-2 space-y-2">
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
            class="inline-block px-4 py-2 rounded-lg text-sm whitespace-pre-line break-words"
            :class="
              msg.sender === 'bot' ? 'bg-gray-700 text-left' : 'bg-blue-600 text-right max-w-[75%]'
            "
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

        <div v-if="loading" class="flex justify-start">
          <div class="px-4 py-2 rounded-lg text-sm bg-gray-700 animate-pulse-bounce">
            <span class="typing-dot">.</span>
            <span class="typing-dot delay-150">.</span>
            <span class="typing-dot delay-300">.</span>
          </div>
        </div>

        <div ref="chatScrollAnchor"></div>
      </transition-group>

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
import { ref, nextTick } from 'vue'
import axios from 'axios'

const isOpen = ref(false)
const input = ref('')
const step = ref(0)
const matricule = ref('')
const student = ref(null)
const rawResults = ref([])
const messages = ref([{ sender: 'bot', text: 'Bienvenue ! Quel est ton matricule ?' }])
const showPulse = ref(true)
const chatScrollAnchor = ref(null)
const loading = ref(false)

let inactivityTimer = null
const AUTO_CLOSE_DELAY = 2 * 60 * 1000 // 1 minutes

function resetInactivityTimer() {
  clearTimeout(inactivityTimer)
  inactivityTimer = setTimeout(() => {
    closeChat()
  }, AUTO_CLOSE_DELAY)
}

function toggleChat() {
  isOpen.value = true
  showPulse.value = false
  resetInactivityTimer()
}

function closeChat() {
  isOpen.value = false
  input.value = ''
  step.value = 0
  matricule.value = ''
  student.value = null
  rawResults.value = []
  messages.value = [{ sender: 'bot', text: 'Bienvenue ! Quel est ton matricule ?' }]
  clearTimeout(inactivityTimer)
  setTimeout(() => {
    showPulse.value = true
  }, 6000)
}

function scrollToBottom() {
  nextTick(() => {
    setTimeout(() => {
      if (chatScrollAnchor.value) {
        chatScrollAnchor.value.scrollIntoView({ behavior: 'smooth' })
      }
    }, 50)
  })
}

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

async function handleSend() {
  if (!input.value.trim()) return

  messages.value.push({ sender: 'user', text: input.value })
  scrollToBottom()
  resetInactivityTimer()

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
    } catch {
      messages.value.push({ sender: 'bot', text: 'Matricule introuvable. Réessaie.' })
    }
    scrollToBottom()
    resetInactivityTimer()
  } else if (step.value >= 1) {
    if (messageText.includes('profil')) {
      loading.value = true
      const start = Date.now()
      scrollToBottom()
      resetInactivityTimer()

      try {
        const res = await axios.get(
          `http://localhost:8000/api/v1/chatbot/student/${student.value.id}/profile`,
        )
        const s = res.data
        const elapsed = Date.now() - start
        await wait(Math.max(1000 - elapsed, 0))
        loading.value = false

        messages.value.push({
          sender: 'bot',
          text: `Nom : ${s.nom}\nPrénom : ${s.prenom}\nSexe : ${s.sexe}\nMatricule : ${s.matricule}\nNiveau : ${s.niveau ?? 'Non spécifié'}`,
        })
        messages.value.push({
          sender: 'bot',
          text: 'Tu peux taper "résultats" ou "fermer".',
        })
      } catch {
        loading.value = false
        messages.value.push({ sender: 'bot', text: 'Erreur lors du chargement du profil.' })
      }
      scrollToBottom()
      resetInactivityTimer()
    } else if (messageText.includes('résultats')) {
      loading.value = true
      const start = Date.now()
      scrollToBottom()
      resetInactivityTimer()

      try {
        const res = await axios.get(
          `http://localhost:8000/api/v1/chatbot/student/${student.value.id}/results`,
        )
        rawResults.value = res.data.results

        const elapsed = Date.now() - start
        await wait(Math.max(1000 - elapsed, 0))
        loading.value = false

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

        messages.value.push({
          sender: 'bot',
          text: 'Tu peux taper "profil" ou "fermer".',
        })
      } catch {
        loading.value = false
        messages.value.push({ sender: 'bot', text: 'Erreur lors du chargement des résultats.' })
      }
      scrollToBottom()
      resetInactivityTimer()
    } else if (messageText.includes('fermer')) {
      closeChat()
    } else {
      messages.value.push({
        sender: 'bot',
        text: 'Je n’ai pas compris. Tu peux taper :\n- "profil" pour voir ton profil\n- "résultats" pour voir tes notes\n- "fermer" pour quitter',
      })
      scrollToBottom()
      resetInactivityTimer()
    }
  }
}
</script>

<style scoped>
.chatbot-button {
  bottom: 1.5rem;
  right: 1.5rem;
}

.chat-enter-active {
  transition: all 0.3s ease-out;
}
.chat-leave-active {
  transition: all 0.2s ease-in;
}
.chat-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.chat-enter-to {
  opacity: 1;
  transform: translateY(0);
}
.chat-leave-from {
  opacity: 1;
  transform: translateY(0);
}
.chat-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.chatbot-pulse {
  background-color: #f97316;
  animation: heartbeat 1.5s infinite;
  position: fixed;
  box-shadow: 0 0 8px rgba(251, 146, 60, 0.7);
}

.chatbot-pulse::after {
  content: '';
  position: fixed;
  width: 100%;
  height: 100%;
  border: 4px solid #c2410c;
  border-radius: 9999px;
  animation: pulse 1.5s ease-out infinite;
  inset: 0;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.6;
  }
  50% {
    transform: scale(1.5);
    opacity: 0;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}

@keyframes heartbeat {
  0%,
  100% {
    transform: scale(1);
  }
  25% {
    transform: scale(0.92);
  }
  50% {
    transform: scale(1.08);
  }
  75% {
    transform: scale(0.98);
  }
}

.typing-dot {
  display: inline-block;
  animation: bounce 1s infinite;
  font-size: 1.5rem;
}

.delay-150 {
  animation-delay: 0.15s;
}
.delay-300 {
  animation-delay: 0.3s;
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}
</style>
