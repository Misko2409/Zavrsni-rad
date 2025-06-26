<template>
  <q-page class="row flex-center q-pa-xl text-center">
    <div>
      <q-icon name="error_outline" color="negative" size="64px" />
      <div class="text-h3 text-negative text-bold q-mt-md">404</div>
      <div class="text-subtitle1 q-mb-md">Oops! Page not found.</div>

      <q-btn
        label="Back to Home"
        color="primary"
        icon="home"
        to="/"
        unelevated
        rounded
      />
    </div>
  </q-page>
</template>

<script setup>
// No logic needed — this is static
</script>

<style scoped>
.q-page {
  background: linear-gradient(to bottom right, #f2f4f8, #ffffff);
  animation: fadeIn 0.6s ease;
}
@keyframes fadeIn {
  from { opacity: 0 }
  to   { opacity: 1 }
}
</style>
