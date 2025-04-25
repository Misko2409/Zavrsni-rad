<template>
  <q-page class="q-pa-md">
    <q-card v-if="meteo && prediction" class="q-pa-md shadow-2" :dark="$q.dark.isActive">
      <q-card-section>
        <div class="text-h6 text-bold text-primary">Trenutni podaci s meteo stanice (Rijeka)</div>
      </q-card-section>

      <q-card-section class="q-gutter-sm">
        <div> Temp: {{ meteo.temperature_2m }} °C</div>
        <div> Vlaga: {{ meteo.relative_humidity_2m }} %</div>
        <div> Tlak: {{ meteo.pressure_msl }} hPa</div>
        <div> Vjetar: {{ meteo.wind_speed_10m }} km/h</div>
        <div> Smjer: {{ meteo.wind_direction_10m }} °</div>
        <div> Oblačnost: {{ meteo.cloudcover }} %</div>
        <div> Oborine: {{ meteo.precipitation }} mm</div>
        <div> Snijeg: {{ meteo.snowfall }} mm</div>
        <div> UV indeks: {{ meteo.uv_index }}</div>
        <div> Dan/Noć: {{ meteo.is_day ? 'Dan' : 'Noć' }}</div>
      </q-card-section>

      <q-separator />

      <q-card-section class="q-mt-md">
        <q-banner class="bg-primary text-white">
          Predikcija: {{ prediction }}
        </q-banner>
      </q-card-section>
    </q-card>

    <q-inner-loading :showing="loading" color="primary" />
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const meteo = ref(null)
const prediction = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    // Dohvati aktualne meteo podatke za Rijeku
    const res = await axios.get(
      'https://api.open-meteo.com/v1/forecast?latitude=45.33&longitude=14.45&current=temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,wind_direction_10m,cloudcover,precipitation,snowfall,uv_index,is_day'
    )

    const data = res.data.current
    meteo.value = data

// Pripremi podatke za model
const now = new Date()
const aiInput = {
temperature_C: Number(data.temperature_2m),
humidity_percent: Number(data.relative_humidity_2m),
pressure_hPa: Number(data.pressure_msl),
wind_speed_kmh: Number(data.wind_speed_10m),
wind_direction_deg: Number(data.wind_direction_10m),
precipitation_mm: Number(data.precipitation),
cloudcover_percent: Number(data.cloudcover),
uv_index: Number(data.uv_index),
snowfall_mm: Number(data.snowfall),
is_day: Number(data.is_day),
hour: now.getHours(),
month: now.getMonth() + 1,
day: now.getDate(),
weekday: now.getDay() === 0 ? 6 : now.getDay() - 1
}


    // Pošalji podatke modelu
    const aiResponse = await axios.post('http://127.0.0.1:5000/predict', aiInput)
    prediction.value = aiResponse.data.prediction
  } catch (err) {
    console.error('[Greška pri dohvaćanju ili predikciji]:', err.response?.data || err.message)
    prediction.value = 'Greška pri predikciji'
  } finally {
    loading.value = false
  }
})
</script>
