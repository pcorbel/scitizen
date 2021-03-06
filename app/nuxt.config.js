export default {
  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  ssr: false,

  // Tell Nuxt to resolve a host address, which is accessible to connections outside of the host machine
  server: {
    port: 80,
    host: '0.0.0.0'
  },

  // Target: https://go.nuxtjs.dev/config-target
  target: 'static',

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: '%s - Scitizen',
    title: 'Scitizen',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' }
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: ['@/assets/main.css'],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://github.com/nuxt-community/vuetify-module
    ['@nuxtjs/vuetify', { treeShake: true }],
    // https://github.com/nuxt-community/moment-module
    '@nuxtjs/moment'
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    // https://i18n.nuxtjs.org
    '@nuxtjs/i18n'
  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {},

  // i18n module configuration: https://i18n.nuxtjs.org/basic-usage
  i18n: {
    locales: [{
      code: 'en',
      file: 'en.js'
    }],
    defaultLocale: 'en',
    lazy: true,
    langDir: 'locales/'
  },

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      dark: false,
      themes: {
        light: {
          primary: '#303F9F',
          secondary: '#C5CAE9',
          accent: '#FFC107'
        }
      }
    }
  },

  loading: {
    color: '#FFC107'
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    analyze: true,
    extractCSS: true,
    babel: {
      plugins: [['@babel/plugin-proposal-private-property-in-object', { loose: true }]]
    }
  }
}
