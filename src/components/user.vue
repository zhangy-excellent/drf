<template>
    <div>
        这是user组件
        <h3>用户列表页</h3>
        <table border="2">
            <tr>
                <td>ID</td>
                <td>姓名</td>
                <td>薪水</td>
                <td>年龄</td>
                <td>操作</td>
            </tr>
            <tr v-for="(person,index) in person_list" :key="index">
                <td>{{person.id}}</td>
                <td>{{person.name}}</td>
                <td>{{person.salary}}</td>
                <td>{{person.age}}</td>
                <td><a href="javascript:;" @click="delete_person">删除</a> | <router-link :to="`/user_detail/${person.id}`">查看详情</router-link></td>
            </tr>
        </table>
        <br>
        <div align="left">
            姓名:<input type="text" v-model="user_name"><br>
            薪水:<input type="number" v-model="user_salary"><br>
            年龄:<input type="number" v-model="user_age"><br>
            <button @click="add_person">提交用户信息</button>
        </div>

    </div>
</template>

<script>
    export default {
        name: "user",
        data: function () {
            return {
                user_name:'',
                user_salary:'',
                user_age:'',

                person_list:localStorage.plist ? JSON.parse(localStorage.plist) :[
                    {'id':1,'name': '张园', 'salary': 19000, 'age': 21},
                    {'id':2,'name': '许金', 'salary': 17000, 'age': 22},
                    {'id':3,'name': '郑卓琳', 'salary': 18000, 'age': 23},
                    {'id':4,'name': 'yy', 'salary': 16000, 'age': 23},
                ]
            }

        },
        methods:{
            delete_person(index){
                this.person_list.splice(index,1)
                localStorage.plist=JSON.stringify(this.person_list)
            },
            add_person(){
                console.log('2321')
                let user_name = this.user_name
                let user_salary = this.user_salary
                let user_age = this.user_age
                let len = this.person_list.length
                let user_id = len+1
                let detail = {id:user_id,name: user_name, salary: user_salary, age: user_age}
                this.person_list.push(detail)
                localStorage.plist=JSON.stringify(this.person_list)
                this.user_name = ''
                this.user_salary = ''
                this.user_age = ''

            }
        }
    }
</script>

<style scoped>

</style>
