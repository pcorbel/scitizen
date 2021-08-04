<template>
  <v-container class="ma-0 pa-0" fluid>
    <v-card flat>
      <v-card-title> Device </v-card-title>

      <!-- CPU Data -->
      <v-card-title>
        <v-row align="center">
          <v-col cols="12" align="center" class="pb-0"> Central Processing Unit </v-col>
          <v-col cols="12" align="center" class="pt-0">
            <v-icon size="64"> mdi-cpu-64-bit </v-icon>
          </v-col>
        </v-row>
      </v-card-title>

      <v-card-text>
        <v-row align="center">
          <v-col> CPU type </v-col>
          <v-col align="right"> {{ this.device.cpu_type }} </v-col>
        </v-row>
        <v-row align="center">
          <v-col> CPU architecure </v-col>
          <v-col align="right">
            {{ this.device.cpu_architecture }}
          </v-col>
        </v-row>
        <v-row align="center">
          <v-col> Number of processors </v-col>
          <v-col align="right">
            {{ this.device.processor_count }}
          </v-col>
        </v-row>
        <v-row align="center">
          <v-col> Operations per second </v-col>
          <v-col align="right">
            {{ this.device.integer_speed_humanized }}OPS
          </v-col>
        </v-row>
        <v-row align="center">
          <v-col> Floating point operations per second </v-col>
          <v-col align="right">
            {{ this.device.floating_point_speed_humanized }}FLOPS
          </v-col>
        </v-row>
      </v-card-text>

      <v-divider />

      <!-- Disk Data -->
      <v-card-title>
        <v-row align="center">
          <v-col cols="12" align="center" class="pb-0"> Disk </v-col>
          <v-col cols="12" align="center" class="pt-0">
            <v-icon size="64"> mdi-harddisk </v-icon>
          </v-col>
        </v-row>
      </v-card-title>

      <v-card-text>
        <v-row align="center">
          <v-col> Total space </v-col>
          <v-col align="right">
            {{ this.device.total_disk_space_humanized }}
          </v-col>
        </v-row>
        <v-row align="center">
          <v-col> Free space </v-col>
          <v-col align="right">
            {{ this.device.free_disk_space_humanized }}
          </v-col>
        </v-row>
        <v-row align="center">
          <v-col> Swap space </v-col>
          <v-col align="right">
            {{ this.device.swap_space_humanized }}
          </v-col>
        </v-row>
      </v-card-text>

      <v-divider />

      <!-- OS Data -->
      <v-card-title>
        <v-row align="center">
          <v-col cols="12" align="center" class="pb-0"> Operating System </v-col>
          <v-col cols="12" align="center" class="pt-0">
            <v-icon size="64"> mdi-linux </v-icon>
          </v-col>
        </v-row>
      </v-card-title>

      <v-card-text>
        <v-row align="center">
          <v-col> Operating system name </v-col>
          <v-col align="right"> {{ this.device.operating_system_name }} </v-col>
        </v-row>
        <v-row align="center">
          <v-col> Operating system version </v-col>
          <v-col align="right">
            {{ this.device.operating_system_version }}
          </v-col>
        </v-row>
        <v-row align="center">
          <v-col> BOINC version </v-col>
          <v-col align="right">
            {{ this.device.boinc_version }}
          </v-col>
        </v-row>
        <v-row align="center">
          <v-col> Scitizen version </v-col>
          <v-col align="right">
            {{ this.device.scitizen_version }}
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  async fetch({ store }) {
    await store.dispatch('devices/fetch')
  },
  computed: {
    device() {
      return this.$store.get('devices/devices')[0]
    },
  },
}
</script>
