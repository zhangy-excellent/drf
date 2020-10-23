<template>
    <div>
        <input type="text" v-model="msg">
        <button @click="add_note">添加留言</button>

        <ul>
            <li v-for="(note,index) in msg_list" :key="index">{{note}}<a href="javascript:;" @click="delete_note(index)">删除</a></li>
        </ul>
        <a href="javascript:;" @click="delete_all_notes" v-show="isShow">删除所有留言</a>
    </div>
</template>

<script>
    export default {
        name: "home",
        data:function () {
            return{
               msg:'',
               msg_list:localStorage.msgs ? JSON.parse(localStorage.msgs) :[],
            }
        },

        created() {
          let len = this.msg_list.length
          if(len)  {
              this.isShow = true
          }
          else{
              this.isShow = false
          }
        },

        methods:{
            add_note(){
                this.isShow = true
                let msg = this.msg
                console.log(this.msg_list,typeof this.msg_list)
                if(msg)
                {
                    this.msg_list.unshift(this.msg)
                    localStorage.msgs = JSON.stringify(this.msg_list)
                    this.msg=''
                }
            },
            delete_note(index){
                this.msg_list.splice(this.msg,1)
                localStorage.msgs = JSON.stringify(this.msg_list)
                console.log(this.msg_list,typeof this.msg_list)
                let len = this.msg_list.length
                if(len){
                    this.isShow = true
                }
                else{
                    this.isShow = false
                }

            },
            delete_all_notes(){
                this.msg_list = []
                localStorage.msgs = JSON.stringify(this.msg_list)
                this.isShow = false
            }
        }
    }
</script>

<style scoped>

</style>
