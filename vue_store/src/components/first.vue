<template>
<div>
    <span>这是第一个组件</span>
    <button @click="add_count">点我长大</button>
</div>
</template>

<script>
    export default {
        // name: "first",
        methods:{
            add_count(){
            this.$store.commit("add_up")
        }
        },

    }
</script>

<style scoped>

</style>
