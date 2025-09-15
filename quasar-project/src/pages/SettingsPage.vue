<template>
  <q-page class="q-pa-md" :dark="$q.dark.isActive">
    <q-card flat bordered class="q-pa-md shadow-2" :dark="$q.dark.isActive">
      <q-card-section class="row items-center q-gutter-sm">
        <q-icon name="settings" size="md" color="primary" />
        <div class="text-h5 text-primary text-bold">Application Settings</div>
      </q-card-section>

      <q-separator class="q-my-sm" />

      <q-card-section>
        <div class="text-subtitle2 text-grey-8 q-mb-md">Appearance</div>

        <!-- Dark Mode Toggle -->
        <q-toggle
          v-model="settingsStore.darkMode"
          :icon="settingsStore.darkMode ? 'light_mode' : 'dark_mode'"
          label="Dark Mode"
          @update:model-value="changeMode"
          class="q-mb-md"
        />

        <!-- Font Size Selector -->
        <q-select
          v-model="settingsStore.fontSize"
          :options="fontSizeOptions"
          label="Font Size"
          @update:model-value="changeFontSize"
          emit-value
          map-options
        />
      </q-card-section>

      <q-separator />
    </q-card>
  </q-page>
</template>

<script setup>
import { LocalStorage, useQuasar } from 'quasar'
import { useSettingsStore } from 'src/stores/settingsStore'

const settingsStore = useSettingsStore()
const $q = useQuasar()

// Available font size options
const fontSizeOptions = [
  { label: 'Small', value: '14px' },
  { label: 'Default', value: '16px' },
  { label: 'Large', value: '18px' },
  { label: 'Extra Large', value: '20px' }
]

// Handle dark mode change
const changeMode = () => {
  LocalStorage.setItem('DarkMode', settingsStore.darkMode)
  $q.dark.set(settingsStore.darkMode)
}

// Handle font size change
const changeFontSize = () => {
  LocalStorage.setItem('FontSize', settingsStore.fontSize)
  document.documentElement.style.setProperty(
    '--app-font-size',
    settingsStore.fontSize
  )
}

// Load saved font size from LocalStorage on page load
const savedSize = LocalStorage.getItem('FontSize')
if (savedSize) {
  settingsStore.fontSize = savedSize
  document.documentElement.style.setProperty('--app-font-size', savedSize)
}
</script>

<style>
/* Apply chosen font size globally */
body {
  font-size: var(--app-font-size, 16px);
}
</style>
