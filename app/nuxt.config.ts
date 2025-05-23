// https://nuxt.com/docs/api/configuration/nuxt-config

export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      COMPANY_NAME: process.env.COMPANY_NAME,
      SITE_NAME: process.env.SITE_NAME,
      SITE_DOMAIN: process.env.SITE_DOMAIN,
      SITE_URL: process.env.SITE_URL,
      MEDIA_URL: process.env.MEDIA_URL,
      API_ALBUM: process.env.API_ALBUM,
      API_ALBUM_COVER: process.env.API_ALBUM_COVER,
      API_CART: process.env.API_CART,
      API_GENRE: process.env.API_GENRE,
      API_LOGOUT: process.env.API_LOGOUT,
      API_MOOD: process.env.API_MOOD,
      API_STATION: process.env.API_STATION,
      API_STATION_PICTURE: process.env.API_STATION_PICTURE,
      API_TRACK: process.env.API_TRACK,
      API_TRACK_PRICE: process.env.API_TRACK_PRICE,
      API_TRACK_EXCLUSIVE_PRICE: process.env.API_TRACK_EXCLUSIVE_PRICE,
      API_TRACK_FAVORITE: process.env.API_TRACK_FAVORITE,
      API_WEB3_LOGIN: process.env.API_WEB3_LOGIN,
      API_WEB3_LOGIN_NONCE: process.env.API_WEB3_LOGIN_NONCE,
    }
  },

  devServer: {
    host: '127.0.0.1',  // Listen on all interfaces (necessary for Docker)
    port: 3000,
  },

  devtools: { enabled: false },

  plugins: ["~/plugins/iconify.ts", "~/plugins/init-cart.client.ts"],

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
