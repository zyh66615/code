// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import store from './store'
import router from './router'
import axios from 'axios'
import ELEMENT from 'element-ui'
import 'default-passive-events'
import CryptoJS from 'crypto-js'

Vue.prototype.$axios = axios
Vue.prototype.CryptoJS = CryptoJS
axios.defaults.withCredentials = true
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
let getCookie = function (cookie) {
  let reg = /csrftoken=([\w]+)[;]?/g
  let res = reg.exec(cookie)[1]
  console.log(res)
  return res
}
axios.interceptors.request.use(
  function (config) {
    // 在post请求前统一添加X-CSRFToken的header信息
    let cookie = document.cookie
    if (cookie && config.method === 'post') {
      config.headers['X-CSRFToken'] = getCookie(cookie)
    }
    return config
  },
  function (error) {
    // Do something with request error
    return Promise.reject(error)
  }
)
Vue.use(ELEMENT)
Vue.config.productionTip = false
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
