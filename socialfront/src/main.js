// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import { i18n } from '@/plugins/i18n'
import Eagle from 'eagle.js'
// import animate.css for slide transition
import 'animate.css'

Vue.use(Eagle)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  i18n,
  Eagle,
  components: { App },
  template: '<App/>'
})
