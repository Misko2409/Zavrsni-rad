<template>
  <q-page class="q-pa-md" :dark="$q.dark.isActive">
    <q-card flat bordered class="q-pa-md shadow-2" :dark="$q.dark.isActive">
      <q-card-section class="row items-center q-gutter-sm">
        <q-icon name="settings" size="md" color="primary" />
        <div class="text-h5 text-primary text-bold">Postavke aplikacije</div>
      </q-card-section>

      <q-separator class="q-my-sm" />

      <q-card-section>
        <div class="text-subtitle2 text-grey-8 q-mb-md">Izgled</div>

        <q-toggle
          v-model="settingsStore.darkMode"
          :icon="settingsStore.darkMode ? 'light_mode' : 'dark_mode'"
          label="Tamni način"
          @update:model-value="changeMode"
          class="q-mb-md"
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

const changeMode = () => {
  LocalStorage.setItem('DarkMode', settingsStore.darkMode)
  $q.dark.set(settingsStore.darkMode)
}
</script>
