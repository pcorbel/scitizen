<template>
  <v-container class="ma-0 pa-0" fluid>
    <v-card flat>
      <v-card-title> {{ $t('nav.projects') }} </v-card-title>

      <!-- The Data Table -->
      <v-data-table
        :headers="headers"
        :items="projects"
        :options="options"
        :items-per-page="20"
        :footer-props="{
          'show-first-last-page': true,
          'items-per-page-options': [20, 50, 100, -1],
        }"
      >
        <!-- Template for avatar -->
        <template v-slot:item.avatar="{ item }">
          <v-avatar color="accent" class="my-2">
            <span class="white--text">{{ item.avatar }}</span>
          </v-avatar>
        </template>

        <!-- Template for Name -->
        <template v-slot:item.name="{ item }">
          <a :href="item.web_url"> {{ item.name }} </a>
        </template>

        <!-- Template for is_active -->
        <template v-slot:item.is_active="{ item }">
          <v-switch
            color="accent"
            @change="sync(item)"
            :input-value="item.is_active"
          />
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
export default {
  async fetch({ store }) {
    await store.dispatch('projects/fetch')
  },
  data() {
    return {
      headers: [
        { text: this.$t('projects.avatar'), value: 'avatar' },
        { text: this.$t('projects.name'), value: 'name' },
        { text: this.$t('projects.specific_area'), value: 'specific_area' },
        { text: this.$t('projects.summary'), value: 'summary' },
        { text: this.$t('projects.home'), value: 'home' },
        { text: this.$t('projects.is_active'), value: 'is_active' },
      ],
      options: {
        sortBy: ['name'],
        sortDesc: [false],
      },
    }
  },
  methods: {
    sync(item) {
      this.$store.dispatch('projects/sync', item)
    },
  },
  computed: {
    projects() {
      return this.$store.get('projects/items')
    },
  },
  head() {
    return {
      title: this.$t('nav.projects'),
    }
  },
}
</script>
