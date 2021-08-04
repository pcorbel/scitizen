<template>
  <v-container class="ma-0 pa-0" fluid>
    <v-card flat>
      <v-card-title> Tasks </v-card-title>

      <!-- The Data Table -->
      <v-data-table
        :headers="headers"
        :items="tasks"
        :options="options"
        @click:row="rowClick"
        single-select
        :items-per-page="20"
        :footer-props="{
          'show-first-last-page': true,
          'items-per-page-options': [20, 50, 100, -1],
        }"
      >
        <!-- Template for State -->
        <template v-slot:item.status="{ item }">
          <v-avatar class="my-2">
            <v-icon :color="item.status.color">
              {{ item.status.icon }}
            </v-icon>
          </v-avatar>
        </template>

        <!-- Template for Project -->
        <template v-slot:item.project_name="{ item }">
          <a :href="item.project_web_url"> {{ item.project_name }} </a>
        </template>

        <!-- Template for ID -->
        <template v-slot:item.id="{ item }">
          <code> {{ item.id }} </code>
        </template>

        <!-- Template for Created -->
        <template v-slot:item.received_at="{ item }">
          {{ item.received_at_humanized }}
        </template>

        <!-- Template for CPU Time -->
        <template v-slot:item.cpu_time="{ item }">
          {{ item.cpu_time_humanized }}
        </template>

        <!-- Template for Finished -->
        <template v-slot:item.completed_at="{ item }">
          {{ item.completed_at_humanized }}
        </template>

        <!-- Template for Progress Bar -->
        <template v-slot:item.fraction_done="{ item }">
          <v-progress-linear
            v-model="item.fraction_done * 100"
            color="accent"
            height="25"
          >
            <template v-slot:default="{ value }">
              <strong> {{ (item.fraction_done * 100).toFixed(2) }}% </strong>
            </template>
          </v-progress-linear>
        </template>
      </v-data-table>
    </v-card>

    <!-- Navigation Drawer -->
    <v-navigation-drawer v-if="selected" app clipped right>
      <v-list>
        <v-list-item>
          <v-spacer />
          <v-list-item-action @click="selected = null">
            <v-btn icon><v-icon> mdi-close </v-icon></v-btn>
          </v-list-item-action>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title> Working Unit Name </v-list-item-title>
            <v-list-item-subtitle>
              {{ selected.name }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title> State </v-list-item-title>
            <v-list-item-subtitle> {{ selected.state }} </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title> Active Task State </v-list-item-title>
            <v-list-item-subtitle>
              {{ selected.active_task_state }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title> Scheduler State </v-list-item-title>
            <v-list-item-subtitle>
              {{ selected.scheduler_state }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title> Last Heartbeat </v-list-item-title>
            <v-list-item-subtitle>
              {{ selected.updated_at_humanized }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title> Deadline </v-list-item-title>
            <v-list-item-subtitle>
              {{ selected.report_deadline_at_humanized }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title> Platform </v-list-item-title>
            <v-list-item-subtitle>
              {{ selected.platform }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title> Exit Statement </v-list-item-title>
            <v-list-item-subtitle>
              {{ selected.exit_statement }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title> Exit Code </v-list-item-title>
            <v-list-item-subtitle>
              {{ selected.exit_code }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title> Elapsed Time </v-list-item-title>
            <v-list-item-subtitle>
              {{ selected.elapsed_time_humanized }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>
              Remaining CPU Time (Estimated)
            </v-list-item-title>
            <v-list-item-subtitle>
              {{ selected.estimated_cpu_time_remaining_humanized }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title> Last Checkpoint CPU Time </v-list-item-title>
            <v-list-item-subtitle>
              {{ selected.checkpoint_cpu_time_humanized }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title> Slot </v-list-item-title>
            <v-list-item-subtitle>
              {{ selected.slot }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title> Process ID </v-list-item-title>
            <v-list-item-subtitle>
              {{ selected.pid }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title> Swap Size </v-list-item-title>
            <v-list-item-subtitle>
              {{ selected.swap_size_humanized }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title> Set Size </v-list-item-title>
            <v-list-item-subtitle>
              {{ selected.set_size_humanized }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title> App Version </v-list-item-title>
            <v-list-item-subtitle>
              {{ selected.version_num }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </v-container>
</template>

<script>
export default {
  async fetch({ store }) {
    await store.dispatch('tasks/fetch')
  },
  data: () => ({
    headers: [
      { text: 'Status', value: 'status' },
      { text: 'Project', value: 'project_name' },
      { text: 'ID', value: 'id' },
      { text: 'Created At', value: 'received_at' },
      { text: 'CPU Time', value: 'cpu_time' },
      { text: 'Finished At', value: 'completed_at' },
      { text: 'Progress', value: 'fraction_done' },
    ],
    options: {
      sortBy: ['status.priority', 'received_at'],
      sortDesc: [false, false],
    },
    polling: null,
    selected: null,
  }),
  created() {
    this.pollData()
  },
  computed: {
    tasks() {
      return this.$store.get('tasks/tasks')
    },
  },
  methods: {
    pollData() {
      this.polling = setInterval(() => {
        this.$store.dispatch('tasks/fetch')
      }, 30000)
    },
    rowClick: function (item, row) {
      row.select(true)
      this.selected = item
    },
  },
  beforeDestroy() {
    clearInterval(this.polling)
  },
}
</script>
