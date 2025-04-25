import { defineStore } from 'pinia'
import { LocalStorage } from 'quasar'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    darkMode: LocalStorage.getItem('DarkMode') ?? false
  }),
  getters: {},
  actions: {}
})
