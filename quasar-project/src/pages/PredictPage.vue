<template>
  <q-page padding>
    <q-form @submit.prevent="submitForm">
      <div class="q-gutter-md">
        <q-input filled v-model="form.temperature_C" label="Temperatura (°C)" />
        <q-input filled v-model="form.humidity_percent" label="Vlaga (%)" />
        <q-input filled v-model="form.pressure_hPa" label="Tlak (hPa)" />
        <q-input filled v-model="form.wind_speed_kmh" label="Brzina vjetra (km/h)" />
        <q-input filled v-model="form.wind_direction_deg" label="Smjer vjetra (°)" />
        <q-input filled v-model="form.precipitation_mm" label="Oborine (mm)" />
        <q-input filled v-model="form.cloudcover_percent" label="Oblačnost (%)" />
        <q-input filled v-model="form.uv_index" label="UV indeks" />
        <q-input filled v-model="form.snowfall_mm" label="Snijeg (mm)" />
        <q-toggle v-model="form.is_day" label="Dan" true-value="1" false-value="0" />
        <q-input filled v-model="form.hour" label="Sat" type="number" />
        <q-input filled v-model="form.month" label="Mjesec" type="number" />
        <q-input filled v-model="form.day" label="Dan" type="number" />
        <q-input filled v-model="form.weekday" label="Dan u tjednu (0=pon)" type="number" />

        <q-btn type="submit" label="Pošalji" color="primary" />
      </div>
    </q-form>

    <div v-if="result" class="q-mt-lg">
      <q-banner class="bg-primary text-white">
        🌦️ Predikcija: {{ result }}
      </q-banner>
    </div>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const form = ref({
  temperature_C: '',
  humidity_percent: '',
  pressure_hPa: '',
  wind_speed_kmh: '',
  wind_direction_deg: '',
  precipitation_mm: '',
  cloudcover_percent: '',
  uv_index: '',
  snowfall_mm: '',
  is_day: 1,
  hour: null,
  month: null,
  day: null,
  weekday: null
})

const result = ref(null)

function convertDecimalsToDot(inputObj) {
  const converted = {}
  for (const key in inputObj) {
    const value = inputObj[key]
    if (typeof value === 'string' && value.includes(',')) {
      converted[key] = parseFloat(value.replace(',', '.'))
    } else {
      converted[key] = typeof value === 'string' ? parseFloat(value) || value : value
    }
  }
  return converted
}

const submitForm = async () => {
  try {
    const payload = convertDecimalsToDot(form.value)

    const response = await axios.post('http://127.0.0.1:5000/predict', payload)
    result.value = response.data.prediction
  } catch (err) {
    result.value = 'Greška pri dohvaćanju predikcije'
    console.error(err)
  }
}
</script>
