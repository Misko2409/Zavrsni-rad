<template>
  <q-page class="q-pa-md">
    <div class="text-center q-mb-xl">
      <div class="text-h4 text-primary text-bold">Welcome to Weather App</div>
      <div class="text-subtitle1 text-grey-8 q-mt-sm">
        Your smart assistant for weather prediction using artificial intelligence.
      </div>
    </div>

    <div class="row q-col-gutter-md justify-center">
      <q-card class="my-card col-xs-12 col-sm-6 col-md-4">
        <q-card-section class="text-center">
          <q-icon name="psychology" size="48px" color="primary" />
          <div class="text-h6 text-bold q-mt-sm">AI Forecast</div>
          <div class="text-subtitle2 text-grey-7 q-mt-xs">
            Enter data manually and get a prediction powered by AI.
          </div>
        </q-card-section>
        <q-card-actions align="center">
          <q-btn color="primary" label="Try Now" to="/predict" />
        </q-card-actions>
      </q-card>

      <q-card class="my-card col-xs-12 col-sm-6 col-md-4">
        <q-card-section class="text-center">
          <q-icon name="autorenew" size="48px" color="primary" />
          <div class="text-h6 text-bold q-mt-sm">Auto AI Forecast</div>
          <div class="text-subtitle2 text-grey-7 q-mt-xs">
            Automatically fetch data from the weather station and get an instant prediction.
          </div>
        </q-card-section>
        <q-card-actions align="center">
          <q-btn color="primary" label="Auto Predict" to="/auto-predict" />
        </q-card-actions>
      </q-card>

      <q-card class="my-card col-xs-12 col-sm-6 col-md-4">
        <q-card-section class="text-center">
          <q-icon name="settings" size="48px" color="primary" />
          <div class="text-h6 text-bold q-mt-sm">Settings</div>
          <div class="text-subtitle2 text-grey-7 q-mt-xs">
            Customize appearance and preferences to suit your needs.
          </div>
        </q-card-section>
        <q-card-actions align="center">
          <q-btn color="primary" label="Settings" to="/settings" />
        </q-card-actions>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
// No background logic needed for basic version
</script>

<style scoped>
.my-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}
.my-card:hover {
  transform: scale(1.02);
}
</style>
