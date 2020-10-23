import Vue from 'vue'
import Router from 'vue-router'
import home from "../components/home";
import user from "../components/user";
import user_detail from "../components/user_detail";

Vue.use(Router)

export default new Router({
  routes: [
    {path: '/home', name: 'home', component: home},
    {path: '/user', name: 'user', component: user},
    {path: '/user_detail/:id', component: user_detail},
    {path: '/', redirect: '/home'},
  ]
})
