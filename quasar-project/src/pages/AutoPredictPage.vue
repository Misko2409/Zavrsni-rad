<template>
  <q-page class="q-pa-md">
    <q-card v-if="meteo && prediction" class="q-pa-md shadow-2" :dark="$q.dark.isActive">
      <q-card-section>
        <div class="text-h6 text-bold text-primary">Current Weather Station Data (Rijeka)</div>
      </q-card-section>

      <q-card-section class="q-gutter-sm">
        <div> Temperature: {{ meteo.temperature_2m }} °C</div>
        <div> Humidity: {{ meteo.relative_humidity_2m }} %</div>
        <div> Pressure: {{ meteo.pressure_msl }} hPa</div>
        <div> Wind Speed: {{ meteo.wind_speed_10m }} km/h</div>
        <div> Wind Direction: {{ meteo.wind_direction_10m }} °</div>
        <div> Cloud Cover: {{ meteo.cloudcover }} %</div>
        <div> Precipitation: {{ meteo.precipitation }} mm</div>
        <div> Snowfall: {{ meteo.snowfall }} mm</div>
        <div> UV Index: {{ meteo.uv_index }}</div>
        <div> Day/Night: {{ meteo.is_day ? 'Day' : 'Night' }}</div>
      </q-card-section>

      <q-separator />

      <q-card-section class="q-mt-md">
        <q-banner class="bg-primary text-white">
          Prediction now: {{ prediction }}
        </q-banner>
      </q-card-section>
    </q-card>

    <q-space />

    <!-- 24h forecast -->
    <q-card v-if="futurePredictions.length" class="q-pa-md q-mt-md shadow-2" :dark="$q.dark.isActive">
      <q-card-section>
        <div class="text-h6 text-bold text-primary">Forecast for the Next 24 Hours</div>
      </q-card-section>

      <q-card-section>
        <q-markup-table dense flat>
          <thead>
            <tr>
              <th>Hour</th>
              <th>Temp (°C)</th>
              <th>Rain Chance</th>
              <th>Icon</th>
              <th>Prediction</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in futurePredictions" :key="index">
              <td>{{ item.hour }}h</td>
              <td>{{ item.temperature }}</td>
              <td>{{ item.rainChance }}%</td>
              <td>{{ getWeatherIcon(item.prediction) }}</td>
              <td>{{ item.prediction }}</td>
            </tr>
          </tbody>
        </q-markup-table>
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
const futurePredictions = ref([])
const loading = ref(true)

// Rain chance estimation based on mm thresholds
function estimateRainChance(mm) {
  if (mm === 0) return 0
  if (mm < 0.1) return 10
  if (mm < 0.5) return 30
  if (mm < 1.0) return 50
  if (mm < 2.5) return 70
  if (mm < 5.0) return 85
  return 100
}

// Icon selector for weather predictions
function getWeatherIcon(prediction) {
  const text = prediction.toLowerCase()

  if (text.includes('vedro') || text.includes('sunčano') || text.includes('clear')) return '☀️'
  if (text.includes('uglavnom vedro')) return '🌤️'
  if (text.includes('djelomično') || text.includes('partly') || text.includes('poluoblačno')) return '🌤️'
  if (text.includes('oblačno') || text.includes('cloudy')) return '☁️'
  if (text.includes('kiša') || text.includes('rain') || text.includes('pljusak')) return '🌧️'
  if (text.includes('grmljavina') || text.includes('thunder')) return '⛈️'
  if (text.includes('snijeg') || text.includes('snow')) return '🌨️'
  if (text.includes('magla') || text.includes('fog')) return '🌫️'
  return '❓'
}


onMounted(async () => {
  try {
    const lat = 45.33
    const lon = 14.45

    // Fetch current and hourly forecast data
    const res = await axios.get(
      `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,wind_direction_10m,cloudcover,precipitation,snowfall,uv_index,is_day&hourly=temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,wind_direction_10m,cloudcover,precipitation,snowfall,uv_index,is_day`
    )

    const current = res.data.current
    const hourly = res.data.hourly

    meteo.value = current

    const now = new Date()
    const currentHourIndex = hourly.time.findIndex(t => new Date(t).getHours() === now.getHours())

    // Current prediction
    const aiInputNow = {
      temperature_C: Number(current.temperature_2m),
      humidity_percent: Number(current.relative_humidity_2m),
      pressure_hPa: Number(current.pressure_msl),
      wind_speed_kmh: Number(current.wind_speed_10m),
      wind_direction_deg: Number(current.wind_direction_10m),
      precipitation_mm: Number(current.precipitation),
      cloudcover_percent: Number(current.cloudcover),
      uv_index: Number(current.uv_index),
      snowfall_mm: Number(current.snowfall),
      is_day: Number(current.is_day),
      hour: now.getHours(),
      month: now.getMonth() + 1,
      day: now.getDate(),
      weekday: now.getDay() === 0 ? 6 : now.getDay() - 1
    }

    const responseNow = await axios.post('http://127.0.0.1:5000/predict', aiInputNow)
    prediction.value = responseNow.data.prediction

    // 24h future predictions
    const future = []
    for (let i = 1; i <= 24; i++) {
      const index = currentHourIndex + i
      if (!hourly.time[index]) break

      const futureDate = new Date(hourly.time[index])
      const input = {
        temperature_C: Number(hourly.temperature_2m[index]),
        humidity_percent: Number(hourly.relative_humidity_2m[index]),
        pressure_hPa: Number(hourly.pressure_msl[index]),
        wind_speed_kmh: Number(hourly.wind_speed_10m[index]),
        wind_direction_deg: Number(hourly.wind_direction_10m[index]),
        precipitation_mm: Number(hourly.precipitation[index]),
        cloudcover_percent: Number(hourly.cloudcover[index]),
        uv_index: Number(hourly.uv_index[index]),
        snowfall_mm: Number(hourly.snowfall[index]),
        is_day: Number(hourly.is_day[index]),
        hour: futureDate.getHours(),
        month: futureDate.getMonth() + 1,
        day: futureDate.getDate(),
        weekday: futureDate.getDay() === 0 ? 6 : futureDate.getDay() - 1
      }

      const aiResponse = await axios.post('http://127.0.0.1:5000/predict', input)

      future.push({
        hour: `${futureDate.getHours()}`,
        prediction: aiResponse.data.prediction,
        temperature: input.temperature_C,
        rainChance: estimateRainChance(input.precipitation_mm)
      })
    }

    futurePredictions.value = future
  } catch (err) {
    console.error('[Error fetching or predicting]:', err.response?.data || err.message)
    prediction.value = 'Prediction error'
  } finally {
    loading.value = false
  }
})
</script>
