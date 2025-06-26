<template>
  <q-page class="q-pa-md relative-position">
    <!-- Animated Weather Background -->
    <div :class="['weather-bg', currentWeatherClass]" />

    <div class="text-center q-mb-xl relative-position" style="z-index: 1">
      <div class="text-h4 text-primary text-bold">Welcome to Weather App</div>
      <div class="text-subtitle1 text-grey-8 q-mt-sm">
        Your smart assistant for weather prediction using artificial intelligence.
      </div>
    </div>

    <div class="row q-col-gutter-md justify-center relative-position" style="z-index: 1">
      <!-- Cards (same as before) -->
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
import { ref, onMounted } from 'vue'
import axios from 'axios'

const currentWeatherClass = ref('weather-bg--clear') // default class

onMounted(async () => {
  try {
    const res = await axios.get(
      'https://api.open-meteo.com/v1/forecast?latitude=45.33&longitude=14.45&current=precipitation,cloudcover,temperature_2m,is_day'
    )

    const data = res.data.current
    const isRain = data.precipitation > 0.3
    const isSnow = data.temperature_2m < 2 && data.precipitation > 0.1
    const isCloudy = data.cloudcover > 70
    const isClear = data.cloudcover < 20

    if (isSnow) currentWeatherClass.value = 'weather-bg--snow'
    else if (isRain) currentWeatherClass.value = 'weather-bg--rain'
    else if (isCloudy) currentWeatherClass.value = 'weather-bg--cloudy'
    else if (isClear) currentWeatherClass.value = 'weather-bg--clear'
    else currentWeatherClass.value = 'weather-bg--default'
  } catch (err) {
    console.error('Weather background fetch failed', err)
  }
})
</script>

<style scoped>
.weather-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  opacity: 0.2;
  pointer-events: none;
  transition: background 1s ease;
}

/* Background classes */
.weather-bg--rain {
  background: url('https://media.giphy.com/media/3o6ZsYcG9JzU0jRnnq/giphy.gif') center center / cover no-repeat;
}
.weather-bg--snow {
  background: url('https://media.giphy.com/media/l3q2K5jinAlChoCLS/giphy.gif') center center / cover no-repeat;
}
.weather-bg--cloudy {
  background: url('https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif') center center / cover no-repeat;
}
.weather-bg--clear {
  background: url('https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif') center center / cover no-repeat;
}
.weather-bg--default {
  background-color: #cccccc;
}
.my-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}
.my-card:hover {
  transform: scale(1.02);
}
</style>
