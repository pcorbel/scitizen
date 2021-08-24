<template>
  <v-container class="ma-0 pa-0" fluid>
    <v-card flat>
      <v-card-title> <v-icon> mdi-linux </v-icon> Device </v-card-title>

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

        <!-- Template for ID -->
        <template v-slot:item.id="{ item }">
          <code> {{ item.id }} </code>
        </template>
      </v-data-table>

      <v-divider />

      <v-card-title> <v-icon> mdi-cpu-64-bit </v-icon> CPU </v-card-title>

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

      <v-card-title> <v-icon> mdi-harddisk </v-icon> Disk </v-card-title>

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
  data: () => ({
    device_headers: [
      { text: 'Name', value: 'name' },
      { text: 'ID', value: 'id' },
      { text: 'Type', value: 'type' },
      { text: 'Operating System', value: 'operating_system_version' },
      { text: 'BOINC Version', value: 'boinc_version' },
      { text: 'Scitizen Version', value: 'scitizen_version' },
    ],
    cpu_headers: [
      { text: 'Architecture', value: 'cpu_architecture' },
      { text: 'Number of Processors', value: 'processor_count' },
      { text: 'Operations per second', value: 'floating_point_speed' },
      { text: 'Floating point operations per second', value: 'integer_speed' },
    ],
    disk_headers: [
      { text: 'Total space', value: 'total_disk_space_humanized' },
      { text: 'Free space', value: 'free_disk_space_humanized' },
      { text: 'Swap space', value: 'swap_space_humanized' },
    ],
  }),
  computed: {
    devices() {
      return this.$store.get('devices/devices')
    },
  },
  head() {
    return {
      title: 'Devices',
    }
  },
}
</script>
