<template>
  <div id="app">
    <nav class="navbar navbar-light bg-light">
      <a class="navbar-brand mr-auto" href="#">
        <img src="@/assets/logo.png" width="30" height="30" class="d-inline-block align-top" alt="">
        SocialGames
      </a>
      <span v-if="getUri()" class="pr-2">{{$t('_code')}}: <b>{{getUri()}}</b></span>
      <a v-if="isLoggedIn()" class="btn btn-outline-success my-2 my-sm-0" href="#/logout">{{$t('log.out')}}</a>
    </nav>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  methods: {
    isLoggedIn () {
      return sessionStorage.getItem('authToken') !== null
    },
    getUri () {
      return this.$route.params.uri
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
