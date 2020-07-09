import Vuex from 'vuex'
import appStore from './app'

export default new Vuex.Store({
  modules: {
    App: appStore
  }
})
