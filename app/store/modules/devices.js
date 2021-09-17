import prettyBytes from 'pretty-bytes'
import { make } from 'vuex-pathify'

function state () {
  return { items: [] }
}

const mutations = {
  ...make.mutations(state)
}

const actions = {
  ...make.actions(state),

  async fetch ({ dispatch }) {
    const apiEndpoint = `${window.location.protocol}//${window.location.hostname}:8080/api/devices`
    const devices = await this.$axios.$get(apiEndpoint)
    dispatch('setItems', devices)
  }
}

const getters = {
  ...make.getters(state),

  devices (state) {
    let devices = JSON.parse(JSON.stringify(state.items))

    // Humanize device
    devices = devices.map((device) => {
      device.integer_speed_humanized = prettyBytes(
        device.integer_speed
      ).slice(0, -1)
      device.floating_point_speed_humanized = prettyBytes(
        device.floating_point_speed
      ).slice(0, -1)
      device.total_disk_space_humanized = prettyBytes(device.total_disk_space)
      device.free_disk_space_humanized = prettyBytes(device.free_disk_space)
      device.swap_space_humanized = prettyBytes(device.swap_space)
      return device
    })

    return devices
  },

  device (state) {
    return state.items.length === 0 ? {} : state.items[0]
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
