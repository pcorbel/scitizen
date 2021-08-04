import { make } from 'vuex-pathify'
import moment from 'moment-timezone'
import prettyBytes from 'pretty-bytes'

function state () {
  return { items: [] }
}

const mutations = {
  ...make.mutations(state)
}

const actions = {
  ...make.actions(state),

  async fetch ({ dispatch }) {
    const apiEndpoint = `${window.location.protocol}//${window.location.hostname}:8080/api/tasks`
    const tasks = await this.$axios.$get(apiEndpoint)
    dispatch('setItems', tasks)
  }
}

const getters = {
  ...make.getters(state),

  tasks (state) {
    let tasks = JSON.parse(JSON.stringify(state.items))
    const running = { color: 'blue', icon: 'mdi-play-circle', priority: 1 }
    const uploading = {
      color: 'blue',
      icon: 'mdi-arrow-up-bold-circle',
      priority: 2
    }
    const downloading = {
      color: 'blue',
      icon: 'mdi-download-circle',
      priority: 3
    }
    const paused = { color: 'grey', icon: 'mdi-pause-circle', priority: 4 }
    const waiting = { color: 'grey', icon: 'mdi-clock', priority: 5 }
    const success = { color: 'green', icon: 'mdi-check-circle', priority: 6 }
    const failed = { color: 'red', icon: 'mdi-stop-circle', priority: 7 }

    // Set icon
    tasks = tasks.map((task) => {
      if (task.completed_at && task.exit_code === 0) {
        task.status = success
      } else if (task.exit_code !== 0) {
        task.status = failed
      } else if (task.state === 'NEW' || task.state === 'FILES_DOWNLOADING') {
        task.status = downloading
      } else if (task.state === 'FILES_UPLOADING') {
        task.status = uploading
      } else if (task.scheduler_state === 'PREEMPTED') {
        task.status = paused
      } else if (task.active_task_state === 'SUSPENDED') {
        task.status = paused
      } else if (task.state === 'FILES_DOWNLOADED' && !task.scheduler_state) {
        task.status = waiting
      } else if (task.active_task_state === 'EXECUTING') {
        task.status = running
      } else if (task.active_task_state === 'UNINITIALIZED') {
        task.status = waiting
      } else if (task.scheduler_state === 'UNINITIALIZED') {
        task.status = waiting
      }

      return task
    })

    // Humanize Time
    moment.tz.setDefault("UTC")
    tasks = tasks.map((task) => {
      if (task.received_at) {
        task.received_at_humanized = moment(task.received_at).format(
          'MMMM Do, YYYY'
        )
      } else {
        task.received_at_humanized = '-'
      }

      if (task.completed_at) {
        task.completed_at_humanized = moment(task.completed_at).format(
          'MMMM Do, YYYY'
        )
      } else {
        task.completed_at_humanized = '-'
      }

      if (task.report_deadline_at) {
        task.report_deadline_at_humanized = moment(task.report_deadline_at).format(
          'MMMM Do, YYYY'
        )
      } else {
        task.report_deadline_at_humanized = '-'
      }

      if (task.elapsed_time) {
        task.elapsed_time_humanized = moment
          .duration(task.elapsed_time, 'seconds')
          .humanize()
      } else {
        task.elapsed_time_humanized = '-'
      }

      if (task.current_cpu_time) {
        task.cpu_time_humanized = moment
          .duration(task.current_cpu_time, 'seconds')
          .humanize()
      } else {
        task.cpu_time_humanized = '-'
      }

      if (task.estimated_cpu_time_remaining) {
        task.estimated_cpu_time_remaining_humanized = moment
          .duration(task.estimated_cpu_time_remaining, 'seconds')
          .humanize()
      } else {
        task.estimated_cpu_time_remaining_humanized = '-'
      }

      if (task.checkpoint_cpu_time) {
        task.checkpoint_cpu_time_humanized = moment
          .duration(task.checkpoint_cpu_time, 'seconds')
          .humanize()
      } else {
        task.checkpoint_cpu_time_humanized = '-'
      }

      if (!task.exit_statement) {
        task.exit_statement = '-'
      }

      if (task._updated_at) {
        task.updated_at_humanized = moment(task._updated_at).fromNow()
      } else {
        task.updated_at_humanized = moment(task.received_at).fromNow()
      }

      return task
    })

    // Humanize Size
    tasks = tasks.map((task) => {
      if (task.set_size) {
        task.set_size_humanized = prettyBytes(task.set_size)
      } else {
        task.set_size_humanized = '-'
      }

      if (task.swap_size) {
        task.swap_size_humanized = prettyBytes(task.swap_size)
      } else {
        task.swap_size_humanized = '-'
      }

      return task
    })

    // Humanize String values
    tasks = tasks.map((task) => {
      if (!task.active_task_state) {
        task.active_task_state = '-'
      }

      if (!task.scheduler_state) {
        task.scheduler_state = '-'
      }

      if (!task.slot) {
        task.slot = '-'
      }

      if (!task.pid) {
        task.pid = '-'
      }

      return task
    })

    return tasks
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
