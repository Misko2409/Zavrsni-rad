<template>
  <q-page padding>
    <q-form @submit.prevent="submitForm">
      <div class="q-gutter-md">
        <q-input filled v-model="form.temperature_C" label="Temperature (°C)" />
        <q-input filled v-model="form.humidity_percent" label="Humidity (%)" />
        <q-input filled v-model="form.pressure_hPa" label="Pressure (hPa)" />
        <q-input filled v-model="form.wind_speed_kmh" label="Wind Speed (km/h)" />
        <q-input filled v-model="form.wind_direction_deg" label="Wind Direction (°)" />
        <q-input filled v-model="form.precipitation_mm" label="Precipitation (mm)" />
        <q-input filled v-model="form.cloudcover_percent" label="Cloud Cover (%)" />
        <q-input filled v-model="form.uv_index" label="UV Index" />
        <q-input filled v-model="form.snowfall_mm" label="Snowfall (mm)" />
        <q-toggle v-model="form.is_day" label="Daytime" true-value="1" false-value="0" />
        <q-input filled v-model="form.hour" label="Hour" type="number" />
        <q-input filled v-model="form.month" label="Month" type="number" />
        <q-input filled v-model="form.day" label="Day" type="number" />
        <q-input filled v-model="form.weekday" label="Weekday (0=Mon)" type="number" />

        <q-btn type="submit" label="Submit" color="primary" />
      </div>
    </q-form>

    <div v-if="result" class="q-mt-lg">
      <q-banner class="bg-primary text-white">
        Prediction: {{ translatePredictionToEnglish(result) }}
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
    result.value = 'Error fetching prediction'
    console.error(err)
  }
}

//Translating from Croatian To English

function translatePredictionToEnglish(prediction) {
  const map = {
  'Vedro': 'Clear',
  'Uglavnom vedro': 'Mostly clear',
  'Djelomično oblačno': 'Partly cloudy',
  'Oblačno': 'Cloudy',

  'Magla': 'Fog',
  'Smrzavajuća magla': 'Freezing fog',

  'Slaba rosulja': 'Slight drizzle',
  'Umjerena rosulja': 'Moderate drizzle',
  'Jaka rosulja': 'Heavy drizzle',

  'Slaba smrzavajuća rosulja': 'Slight freezing drizzle',
  'Jaka smrzavajuća rosulja': 'Heavy freezing drizzle',

  'Slaba kiša': 'Slight rain',
  'Umjerena kiša': 'Moderate rain',
  'Jaka kiša': 'Heavy rain',

  'Slaba smrzavajuća kiša': 'Slight freezing rain',
  'Jaka smrzavajuća kiša': 'Heavy freezing rain',

  'Slab snijeg': 'Slight snow',
  'Umjeren snijeg': 'Moderate snow',
  'Jak snijeg': 'Heavy snow',
  'Zrnca snijega': 'Snow grains',

  'Slabi pljuskovi': 'Slight showers',
  'Umjereni pljuskovi': 'Moderate showers',
  'Jaki pljuskovi': 'Heavy showers',

  'Slabi snježni pljuskovi': 'Slight snow showers',
  'Jaki snježni pljuskovi': 'Heavy snow showers',

  'Grmljavina': 'Thunderstorm',
  'Grmljavina s malo tuče': 'Thunderstorm with slight hail',
  'Grmljavina s jakom tučom': 'Thunderstorm with heavy hail',

  'Nepoznato': 'Unknown'
}


  return map[prediction] || prediction
}

</script>
