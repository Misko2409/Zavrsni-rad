<template>
  <q-page class="q-pa-md">
    <q-card v-if="meteo && prediction" class="q-pa-md shadow-2" :dark="$q.dark.isActive">
      <q-card-section class="row items-start q-gutter-md">
        <div class="col">
          <div class="text-h6 text-bold text-primary">Current Weather Station Data (Rijeka)</div>

          <div class="q-mt-md">
            <div>Temperature: {{ meteo.temperature_2m }} °C</div>
            <div>Humidity: {{ meteo.relative_humidity_2m }} %</div>
            <div>Pressure: {{ meteo.pressure_msl }} hPa</div>
            <div>Wind Speed: {{ meteo.wind_speed_10m }} km/h</div>
            <div>Wind Direction: {{ meteo.wind_direction_10m }} °</div>
            <div>Cloud Cover: {{ meteo.cloudcover }} %</div>
            <div>Precipitation: {{ meteo.precipitation }} mm</div>
            <div>Snowfall: {{ meteo.snowfall }} mm</div>
            <div>UV Index: {{ meteo.uv_index }}</div>
            <div>Day/Night: {{ meteo.is_day ? 'Day' : 'Night' }}</div>
          </div>

          <q-banner class="bg-primary text-white q-mt-md">
            Prediction now: {{ translatePredictionToEnglish(prediction) }}
          </q-banner>
        </div>

        <div class="col-auto">
          <img
            v-if="prediction"
            :src="getWeatherGif(prediction, meteo.is_day)"
            alt="Weather Icon"
            style="width: 120px; height: 120px"
          />
        </div>
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
              <td>
                <img
                  :src="getWeatherGif(item.prediction, item.is_day)"
                  alt="icon"
                  style="width: 40px; height: 40px"
                />
              </td>
              <td>{{ translatePredictionToEnglish(item.prediction) }}</td>

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

function estimateRainChance(mm) {
  if (mm === 0) return 0
  if (mm < 0.1) return 10
  if (mm < 0.5) return 30
  if (mm < 1.0) return 50
  if (mm < 2.5) return 70
  if (mm < 5.0) return 85
  return 100
}

function getWeatherGif(prediction, isDay) {
  const text = prediction.toLowerCase()
  const daynight = isDay ? 'day' : 'night'

  if (text.includes('vedro') || text.includes('clear')) return `/animations/clear_${daynight}.gif`
  if (text.includes('uglavnom vedro')) return `/animations/clear_${daynight}.gif`
  if (text.includes('djelomično') || text.includes('partly')) return `/animations/cloudy_${daynight}.gif`
  if (text.includes('oblačno') || text.includes('cloudy')) return `/animations/cloudy_${daynight}.gif`
  if (text.includes('kiša') || text.includes('rain') || text.includes('pljusak')) return `/animations/rain_${daynight}.gif`
  if (text.includes('grmljavina') || text.includes('thunder')) return `/animations/thunder_${daynight}.gif`
  if (text.includes('snijeg') || text.includes('snow')) return `/animations/snow_${daynight}.gif` // ADD SNOW NIGHT PICTURE
  if (text.includes('magla') || text.includes('fog')) return `/animations/fog_${daynight}.gif`
  return `/animations/default.gif`
}

onMounted(async () => {
  try {
    const lat = 45.33
    const lon = 14.45

    const res = await axios.get(
      `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,wind_direction_10m,cloudcover,precipitation,snowfall,uv_index,is_day&hourly=temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,wind_direction_10m,cloudcover,precipitation,snowfall,uv_index,is_day`
    )

    const current = res.data.current
    const hourly = res.data.hourly

    meteo.value = current

    const now = new Date()
    const currentHourIndex = hourly.time.findIndex(t => new Date(t).getHours() === now.getHours())

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
        rainChance: estimateRainChance(input.precipitation_mm),
        is_day: input.is_day
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

function translatePredictionToEnglish(prediction) {
  const map = {
    'Vedro': 'Clear',
    'Sunčano': 'Sunny',
    'Uglavnom vedro': 'Mostly clear',
    'Djelomično oblačno': 'Partly cloudy',
    'Poluoblačno': 'Partly cloudy',
    'Oblačno': 'Cloudy',
    'Kiša': 'Rain',
    'Pljusak': 'Shower',
    'Grmljavina': 'Thunderstorm',
    'Snijeg': 'Snow',
    'Magla': 'Fog',
    'Slaba kiša': 'Slight Rain',
    'Umjerena kiša': 'Moderate Rain',
    'Umjerena rosulja': 'Moderate Drizzle',
    'Slaba rosulja': 'Slight Drizzle',
    'Jaka rosulja': 'Heavy Drizzle',
    'Jaka kiša': 'Heavy Rain',
    'Nepoznato': 'Unknown'
  }

  return map[prediction] || prediction
}

</script>
