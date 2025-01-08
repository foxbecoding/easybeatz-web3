// https://nuxt.com/docs/api/configuration/nuxt-config

export default defineNuxtConfig({
  devServer: {
    host: '0.0.0.0',  // Listen on all interfaces (necessary for Docker)
    port: 3000,
  },

  devtools: { enabled: false },

  plugins: ["~/plugins/iconify.ts"],

  modules: [
    '@nuxtjs/tailwindcss',
    '@nuxtjs/color-mode',
    [
      '@pinia/nuxt',
      {
        autoImports: [
          'defineStore',
          'acceptHMRUpdate',
        ],
      },
    ]
  ],

  //colorMode: {
  //  preference: 'system', // default theme
  //  dataValue: 'theme', // activate data-theme in <html> tag
  //  classSuffix: '',
  //},
  tailwindcss: { exposeConfig: true },

  compatibilityDate: '2025-01-03',

  alias: {

    '~': './'

  }
})
