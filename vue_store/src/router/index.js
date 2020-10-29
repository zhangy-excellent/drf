import Vue from 'vue'
import router from 'vue-router'
import App from "../App";

Vue.use(router)

export default new router({
  routes: [
      {path:'/',component:App}
  ]
})
