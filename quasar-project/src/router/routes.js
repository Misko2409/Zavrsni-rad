const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('pages/IndexPage.vue'),
      },
      {
        path: 'contacts',
        name: 'Contacts',
        component: () => import('pages/ContactsPage.vue'),
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('pages/SettingsPage.vue'),
      },
      {
        path: 'predict',
        name: 'Predict',
        component: () => import('pages/PredictPage.vue'),
      },
      { path: 'auto-predict',
        name: "Auto Predict",
        component: () => import('pages/AutoPredictPage.vue'),
      },
    ],
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  }
]

export default routes
