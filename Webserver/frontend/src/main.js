// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import store from './store/store'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import HighchartsVue from 'highcharts-vue'
import 'echarts'
import ECharts from 'vue-echarts' // refers to components/ECharts.vue in webpack

// register component to use
Vue.component('v-chart', ECharts)
Vue.prototype.$EventBus = new Vue()
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(HighchartsVue)
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
