<template>
    <div>
        <router-link to="/home">返回home组件</router-link>
    <router-link to="/user">返回user组件</router-link>
    <br>
    正在查看id为{{$route.params.id}}的学生:<br>
    <router-view></router-view>
    </div>

</template>

<script>
    export default {
        name: "user_detail"
    }
</script>

<style scoped>

</style>
