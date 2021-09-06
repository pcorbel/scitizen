<template>
  <v-container class="ma-0 pa-0" fluid>
    <v-card flat>
      <v-card-title> <v-icon> mdi-linux </v-icon> {{ $t('devices.device.title') }} </v-card-title>

      <!-- The Device Data Table -->
      <v-data-table
        :headers="device_headers"
        :items="devices"
        hide-default-footer
      >
        <!-- Template for Name -->
        <template v-slot:item.name="{ item }">
          <v-chip label color="accent"> {{ item.name }} </v-chip>
        </template>

        <!-- Template for UUID -->
        <template v-slot:item.uuid="{ item }">
          <code> {{ item.uuid }} </code>
        </template>
      </v-data-table>

      <v-divider />

      <v-card-title> <v-icon> mdi-cpu-64-bit </v-icon> {{ $t('devices.cpu.title') }} </v-card-title>

      <!-- The CPU Data Table -->
      <v-data-table :headers="cpu_headers" :items="devices" hide-default-footer>
        <!-- Template for Architecture -->
        <template v-slot:item.cpu_architecture="{ item }">
          <v-chip label color="accent">
            {{ item.cpu_architecture }} ({{ item.name }} )
          </v-chip>
        </template>

        <!-- Template for Integer Speed -->
        <template v-slot:item.integer_speed="{ item }">
          {{ item.integer_speed_humanized }}OPS
        </template>

        <!-- Template for Floating Point Speed -->
        <template v-slot:item.floating_point_speed="{ item }">
          {{ item.floating_point_speed_humanized }}OPS
        </template>
      </v-data-table>

      <v-divider />

      <v-card-title> <v-icon> mdi-harddisk </v-icon> {{ $t('devices.disk.title') }} </v-card-title>

      <!-- The Disk Data Table -->
      <v-data-table
        :headers="disk_headers"
        :items="devices"
        hide-default-footer
      >
      </v-data-table>

      <v-divider />
    </v-card>
  </v-container>
</template>

<script>
export default {
  async fetch({ store }) {
    await store.dispatch('devices/fetch')
  },
  data() {
    return {
      device_headers: [
        { text: this.$t('devices.device.name'), value: 'name' },
        { text: this.$t('devices.device.uuid'), value: 'uuid' },
        { text: this.$t('devices.device.type'), value: 'type' },
        { text: this.$t('devices.device.operating_system_version'), value: 'operating_system_version' },
        { text: this.$t('devices.device.boinc_version'), value: 'boinc_version' },
        { text: this.$t('devices.device.scitizen_version'), value: 'scitizen_version' },
      ],
      cpu_headers: [
        { text: this.$t('devices.cpu.cpu_architecture'), value: 'cpu_architecture' },
        { text: this.$t('devices.cpu.processor_count'), value: 'processor_count' },
        { text: this.$t('devices.cpu.floating_point_speed'), value: 'floating_point_speed' },
        { text: this.$t('devices.cpu.integer_speed'), value: 'integer_speed' },
      ],
      disk_headers: [
        { text: this.$t('devices.disk.total_disk_space_humanized'), value: 'total_disk_space_humanized' },
        { text: this.$t('devices.disk.free_disk_space_humanized'), value: 'free_disk_space_humanized' },
        { text: this.$t('devices.disk.swap_space_humanized'), value: 'swap_space_humanized' },
      ],
    }
  },
  computed: {
    devices() {
      return this.$store.get('devices/devices')
    },
  },
  head() {
    return {
      title: this.$t('nav.devices')
    }
  },
}
</script>
