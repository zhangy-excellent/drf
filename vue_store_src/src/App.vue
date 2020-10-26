<template>
<div id="app">
<first></first>
<second></second>
</div>
</template>

<script>
import first from "./components/first";
import second from "./components/second";
export default {
name: 'App',
components:
{
    first:first,
    second:second
},

}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
