import Vue from 'vue'
import App from './App.vue'

import BootstrapVue from 'bootstrap-vue'

import axios from 'axios';
import VueAxios from 'vue-axios';
import router from './router' //追加

Vue.use(BootstrapVue, axios, VueAxios);

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false

new Vue({
  router, //追加
  render: h => h(App),
}).$mount('#app')
