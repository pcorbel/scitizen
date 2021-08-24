<template>
  <nav>
    <!-- App Bar -->
    <v-app-bar color="primary" app dark flat clipped-left clipped-right>
      <v-container fluid>
        <v-row align="center">
          <!-- Icon -->
          <v-app-bar-nav-icon to="/" nuxt active-class="no-active">
            <v-img
              :src="require(`@/assets/images/planet.svg`)"
              max-width="32px"
            />
          </v-app-bar-nav-icon>
          <v-spacer />
          <!-- Device Name -->
          <nuxt-link to="/devices" class="white--text">
            <strong> {{ this.device.name }} </strong>
          </nuxt-link>
        </v-row>
      </v-container>
    </v-app-bar>

    <!-- Navigation Drawer -->
    <v-navigation-drawer app clipped expand-on-hover>
      <v-list class="my-0">
        <v-list-item to="/tasks" nuxt>
          <v-list-item-icon>
            <v-icon> mdi-checkbox-multiple-marked </v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title> Tasks </v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item to="/projects" nuxt>
          <v-list-item-icon>
            <v-icon> mdi-book-multiple </v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title> Projects </v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item to="/devices" nuxt>
          <v-list-item-icon>
            <v-icon> mdi-raspberry-pi </v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title> Devices </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </nav>
</template>

<script>
export default {
  async fetch() {
    await this.$store.dispatch('devices/fetch')
  },
  computed: {
    device() {
      return this.$store.get('devices/device')
    },
  },
}
</script>
