<template>
  <q-layout
    view="lHh Lpr lFf"
    :class="$q.dark.isActive ? 'bg-dark text-white' : 'bg-grey-2 text-dark'"
  >
    <!-- Header -->
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn flat dense round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" />
        <q-toolbar-title class="cursor-pointer row items-center" @click="goToHome">
          <q-icon name="event" class="q-mr-sm" />
          MyEventUp
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <!-- Drawer -->
    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      :class="$q.dark.isActive ? 'bg-dark text-white' : 'bg-white text-dark'"
      :dark="$q.dark.isActive"
    >
      <q-list>
        <q-item-label header class="text-primary">Navigacija</q-item-label>
        <EssentialLink title="AI Predikcija" to="predict" />
        <EssentialLink title="AI Auto" to="auto-predict" />
        <EssentialLink title="Settings" to="settings" />
        <EssentialLink title="Contacts" to="contacts" />
        <EssentialLink title="ShareApp" to="ShareApp" />
      </q-list>
    </q-drawer>

    <!-- Page content -->
    <q-page-container>
      <router-view />
    </q-page-container>

    <!-- Footer -->
    <q-footer
      class="bg-grey-3 text-dark q-pa-sm text-center"
      :class="$q.dark.isActive ? 'bg-dark text-white' : ''"
      :dark="$q.dark.isActive"
    >
      EventUp! MM AS
    </q-footer>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import EssentialLink from 'components/EssentialLink.vue'

const router = useRouter()
const leftDrawerOpen = ref(false)

const goToHome = () => {
  router.push('/')
}

function toggleLeftDrawer () {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
</script>

<style scoped>
.q-toolbar-title {
  font-weight: bold;
  font-size: 18px;
}
.q-footer {
  font-size: 12px;
}
</style>
