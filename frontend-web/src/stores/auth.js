// stores/auth.js
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('access_token') || null,
    userId: null,
    nom: null,
    prenom: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },
  actions: {
    async login(matricule, password) {
      try {
        const response = await axios.post('http://localhost:8000/api/v1/auth/login', {
          matricule,
          password,
        })

        this.accessToken = response.data.access_token
        localStorage.setItem('access_token', this.accessToken)

        const config = {
          headers: { Authorization: `Bearer ${this.accessToken}` },
        }
        const userResponse = await axios.get('http://localhost:8000/api/v1/students/me', config)

        this.userId = userResponse.data.id
        this.nom = userResponse.data.nom
        this.prenom = userResponse.data.prenom
        return userResponse.data
      } catch (error) {
        this.logout()
        throw error
      }
    },
    logout() {
      this.accessToken = null
      this.userId = null
      this.nom = null
      localStorage.removeItem('access_token')
    },
  },
})
