<!--components/ChatBot.vue-->
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
        <span v-if="showPulse" class="text-[10px]">Appuyez ici !</span>
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
        <button @click="closeChat()" class="text-gray-400 hover:text-white">✖</button>
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
            class="inline-block px-4 py-2 rounded-lg text-sm max-w-[75%]"
            :class="msg.sender === 'bot' ? 'bg-gray-700 text-left' : 'bg-blue-600 text-right'"
          >
            <div
              v-if="msg.html"
              class="bot-html-message whitespace-pre-wrap break-words"
              v-html="msg.html"
            ></div>
            <span v-else class="whitespace-pre-wrap break-words">{{ msg.text }}</span>
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
          <div class="relative flex-1">
            <input
              v-model="input"
              :type="isPasswordStep && !showPassword ? 'password' : 'text'"
              placeholder="Écris ici..."
              class="w-full p-2 pr-10 rounded-lg bg-gray-800 text-white border border-gray-600 focus:outline-none"
            />
            <button
              v-if="isPasswordStep"
              type="button"
              class="absolute inset-y-0 right-2 flex items-center text-gray-400 hover:text-white"
              @click="showPassword = !showPassword"
            >
              <span v-if="showPassword">🙈</span>
              <span v-else>👁️</span>
            </button>
          </div>

          <button
            type="submit"
            :disabled="!canSend"
            :class="[
              'px-4 py-2 rounded-lg text-white transition-colors',
              canSend ? 'bg-blue-600 hover:bg-blue-700' : 'bg-gray-600 cursor-not-allowed',
            ]"
          >
            ➤
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
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
const MESSAGE_COOLDOWN = 2000 // 2 seconde entre deux envois
const showPassword = ref(false)
const isPasswordStep = computed(() => step.value === 0.5)
const MAX_MESSAGE_LENGTH = 26

let inactivityTimer = null
const AUTO_CLOSE_DELAY = 2 * 60 * 1000 // 2 minutes

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

function closeChat(force = false) {
  if (!force && !confirm('Es-tu sûr de vouloir fermer le chatbot ?')) return
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

async function typeBotMessage(fullText) {
  const delay = 20
  const msg = { sender: 'bot', html: '' }
  messages.value.push(msg)
  await nextTick()

  const words = fullText.split(/(\s+)/) // garde les espaces
  let index = 0
  const result = []

  for (const word of words) {
    if (word === '\n') {
      result.push('<br>')
    } else if (word.trim() === '') {
      result.push(word) // espace
    } else {
      const spans = word
        .split('')
        .map(
          (char) =>
            `<span class="drop-letter" style="animation-delay:${index * delay}ms">${char}</span>`,
        )
        .join('')
      result.push(`<span class="word">${spans}</span>`)
      index += word.length
    }
  }

  msg.html = result.join('')
  scrollToBottom()
}

let lastMessageTime = 0
const canSend = ref(true)

async function handleSend() {
  if (!canSend.value || !input.value.trim() || input.value.length > MAX_MESSAGE_LENGTH) return
  const now = Date.now()
  if (now - lastMessageTime < MESSAGE_COOLDOWN || !input.value.trim()) return
  lastMessageTime = now
  canSend.value = false
  setTimeout(() => {
    canSend.value = true
  }, MESSAGE_COOLDOWN)

  const cleanedInput = input.value.replace(/[<>{}[\]\\]/g, '')
  messages.value.push({
    sender: 'user',
    text: step.value === 0.5 ? '••••••••' : cleanedInput,
  })

  scrollToBottom()
  resetInactivityTimer()

  const userInput = cleanedInput.trim()
  input.value = ''
  const messageText = userInput.toLowerCase()

  if (step.value === 0) {
    matricule.value = userInput
    await typeBotMessage('Merci. Quel est ton mot de passe ?')
    step.value = 0.5
    return
  }

  if (step.value === 0.5) {
    try {
      const res = await axios.post('http://localhost:8000/api/v1/chatbot/login', {
        matricule: matricule.value,
        password: userInput,
      })
      student.value = { id: res.data.id, matricule: res.data.matricule }
      step.value = 1

      // ✅ Synchroniser avec le store principal
      await authStore.login(matricule.value, userInput)

      await typeBotMessage(
        `Bonjour ${res.data.prenom} ! Veux-tu voir ton "profil" ou tes "résultats" ?`,
      )
      // eslint-disable-next-line no-unused-vars
    } catch (error) {
      await typeBotMessage('Échec de connexion. Vérifie ton matricule et ton mot de passe.')
      step.value = 0
      matricule.value = ''
    }
    scrollToBottom()
    return
  }

  if (step.value >= 1) {
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

        await typeBotMessage(
          `Nom : ${s.nom}\nPrénom : ${s.prenom}\nSexe : ${s.sexe}\nMatricule : ${s.matricule}\nNiveau : ${s.niveau ?? 'Non spécifié'}`,
        )
        await typeBotMessage('Tu peux taper "résultats" ou "fermer".')
      } catch {
        loading.value = false
        await typeBotMessage('Erreur lors du chargement du profil.')
      }
      scrollToBottom()
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
          await typeBotMessage(ueText)
        }

        if (res.data.average !== null) {
          await typeBotMessage(`Moyenne pondérée : ${res.data.average}`)
        }

        await typeBotMessage('Tu peux taper "profil" ou "fermer".')
      } catch {
        loading.value = false
        await typeBotMessage('Erreur lors du chargement des résultats.')
      }
      scrollToBottom()
    } else if (messageText.includes('fermer')) {
      if (confirm('Es-tu sûr de vouloir fermer le chatbot ?')) closeChat(true)
    } else {
      await typeBotMessage(
        'Je n’ai pas compris. Tu peux taper :\n- "profil" pour voir ton profil\n- "résultats" pour voir tes notes\n- "fermer" pour quitter',
      )
      scrollToBottom()
      resetInactivityTimer()
    }
  }
}
</script>

<style>
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

@keyframes drop-fade {
  0% {
    opacity: 0;
    transform: translateY(-10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.drop-letter {
  display: inline-block;
  opacity: 0;
  animation: drop-fade 0.3s ease forwards;
  white-space: pre;
  word-break: break-word;
}

.message-placeholder {
  min-height: 1rem;
  display: inline-block;
}

/* Empêche la coupure des mots inappropriée */
div[innerHTML],
.bot-html-message {
  white-space: pre-wrap;
  word-break: break-word;
  overflow-wrap: break-word;
  line-height: 1.4;
}

.word {
  display: inline-block;
  white-space: nowrap;
}
</style>
