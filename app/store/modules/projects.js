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
    const apiEndpoint = `${window.location.protocol}//${window.location.hostname}:8080/api/projects`
    const projects = await this.$axios.$get(apiEndpoint)
    dispatch('setItems', projects)
  },

  async sync (_, item) {
    const result = JSON.parse(JSON.stringify(item))
    result.is_active = !result.is_active
    await this.$axios.$post(
      `${process.env.apiEndpoint}/project/${result.id}`,
      result
    )
  }
}

const getters = {
  ...make.getters(state)
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
