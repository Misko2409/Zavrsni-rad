<template>
  <!-- Interni linkovi -->
  <q-item clickable :to="`/${props.to}`" v-if="iconMap[props.to]">
    <q-item-section avatar>
      <q-icon :name="iconMap[props.to]" />
    </q-item-section>
    <q-item-section>
      <q-item-label>{{ props.title }}</q-item-label>
    </q-item-section>
  </q-item>

  <!-- Share aplikacije -->
  <q-item v-else-if="props.to === 'ShareApp'" clickable @click="onShareApp">
    <q-item-section avatar>
      <q-icon name="share" />
    </q-item-section>
    <q-item-section>
      <q-item-label>{{ props.title }}</q-item-label>
    </q-item-section>
  </q-item>
</template>

<script setup>
import { useQuasar } from 'quasar'

const $q = useQuasar()

const props = defineProps({
  title: { type: String, required: true },
  to: { type: String, required: true }
})

const iconMap = {
  'settings': 'settings',
  'contacts': 'contact_mail',
  'predict': 'psychology_alt',
  'auto-predict': 'cloud_sync'
}

const onShareApp = () => {
  const platform = $q.platform.is
  const message = "Link to application 'EventUp " +
    (platform.android ? 'Android' : platform.ios ? 'iOS' : 'web')

  if (window.plugins?.socialsharing) {
    window.plugins.socialsharing.share(message)
  } else {
    console.error('SocialSharing plugin is not available')
  }
}
</script>
