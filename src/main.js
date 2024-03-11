// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import { i18n } from '@/plugins/i18n'

Vue.config.productionTip = false
Vue.prototype.$backend = '192.168.0.102:8000'
Vue.prototype.$colors = ['#fd7e14', '#007bff', '#6f42c1', '#28a745', '#17a2b8']

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  i18n,
  components: { App },
  template: '<App/>'
})
