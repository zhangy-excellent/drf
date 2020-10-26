//导包
import Vue from "vue";
import Vuex from 'vuex'

//将vuex注入到vue实例中
Vue.use(Vuex)

export default new Vuex.Store({
        state:{
            count:1
        },
        mutations:{
            add_up(state){
            state.count++
        },
        },
        getters:{},
})
