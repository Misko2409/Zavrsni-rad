<template>
  <q-page class="q-pa-md" :class="$q.dark.isActive ? 'bg-dark text-white' : 'bg-grey-1'">
    <q-card flat bordered class="shadow-2" :dark="$q.dark.isActive">
      <!-- Contact Title -->
      <q-card-section class="row items-center q-gutter-sm">
        <q-icon name="location_on" size="md" color="primary" />
        <div class="text-h6 text-primary text-bold">Contact Location</div>
      </q-card-section>

      <!-- Contact Info -->
      <q-card-section class="q-gutter-sm">
        <div>📍 <strong>Address:</strong> Fiumara 1, 51000 Rijeka</div>
        <div>📧 <strong>Email:</strong> WeatherApp@support.com</div>
        <div>📞 <strong>Phone:</strong> +385 51 123 456</div>
        <div>⏰ <strong>Working Hours:</strong> Mon – Fri: 08:00 – 16:00</div>
      </q-card-section>

      <!-- Google Map -->
      <GoogleMap
        api-key="AIzaSyDBjFA-VuJtFfhW9cYiu896WArxtAmuG0k"
        style="width: 100%; height: 500px; border-radius: 12px; overflow: hidden"
        :center="center"
        :zoom="15"
        language="en"
      >
        <Marker :options="{ position: center }" @click="infoWindow = true" />
        <InfoWindow :options="{ position: center }" v-if="infoWindow">
          <div class="text-black" style="max-width: 250px">
            <div class="text-bold text-primary">Weather App HQ</div>
            <div>Fiumara 1<br />51000 Rijeka</div>
            <q-btn
              dense
              color="primary"
              icon="navigation"
              outline
              class="q-mt-sm"
              label="Directions"
              @click="onClickDirection"
            />
          </div>
        </InfoWindow>
      </GoogleMap>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { GoogleMap, Marker, InfoWindow } from 'vue3-google-map'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const infoWindow = ref(false)
const center = { lat: 45.326032, lng: 14.446152 }

const onSuccess = (position) => {
  cordova.InAppBrowser.open(
    `https://www.google.com/maps/dir/${position.coords.latitude},${position.coords.longitude}/${center.lat},${center.lng}`,
    '_system',
    'location=yes',
  )
}

const onError = (error) => {
  $q.notify({
    color: 'negative',
    message: `Error: ${error.message}`,
    icon: 'error',
  })
}

const onClickDirection = () => {
  navigator.geolocation.getCurrentPosition(onSuccess, onError)
  infoWindow.value = false
}
</script>
