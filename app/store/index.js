import pathify from './pathify'
import devices from './modules/devices'
import projects from './modules/projects'
import tasks from './modules/tasks'

export const plugins = [pathify.plugin]
export const modules = {
  devices,
  projects,
  tasks
}
