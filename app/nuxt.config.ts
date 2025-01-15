// https://nuxt.com/docs/api/configuration/nuxt-config

export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      COMPANY_NAME: process.env.COMPANY_NAME,
      SITE_NAME: process.env.SITE_NAME,
      SITE_DOMAIN: process.env.SITE_DOMAIN,
      SITE_URL: process.env.SITE_URL,
      API_WEB3_LOGIN: process.env.API_WEB3_LOGIN,
      API_WEB3_LOGIN_NONCE: process.env.API_WEB3_LOGIN_NONCE,
      API_STATION: process.env.API_STATION,
    }
  },

  devServer: {
    host: '0.0.0.0',  // Listen on all interfaces (necessary for Docker)
    port: 3000,
  },

  devtools: { enabled: false },

  plugins: ["~/plugins/iconify.ts"],

  modules: ['@nuxtjs/tailwindcss', '@nuxtjs/color-mode', [
    '@pinia/nuxt',
    {
      autoImports: [
        'defineStore',
        'acceptHMRUpdate',
      ],
    },
  ], '@nuxt/image'],

  tailwindcss: { exposeConfig: true },

  compatibilityDate: '2025-01-03',

  alias: {

    '~': './'

  }
})