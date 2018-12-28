<template>
  <div id="app" class="d-flex flex-column flex-grow-1">
    <nav class="navbar navbar-light bg-light">
      <a class="navbar-brand mr-auto" href="#">
        <img src="@/assets/logo.png" width="30" height="30" class="d-inline-block align-top" alt="">
        {{$t('app.name')}}
      </a>
      <LocaleChanger/>
      <span v-if="getUri()" class="pr-2">{{$t('_code')}}: <b>{{getUri()}}</b></span>
      <a v-if="isLoggedIn()" class="btn btn-outline-success my-2 my-sm-0" href="#/logout">{{$t('log.out')}}</a>
    </nav>
    <router-view/>
  </div>
</template>

<script>
import LocaleChanger from './components/LocaleChanger.vue'

export default {
  components: {
    LocaleChanger
  },
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
  height: inherit;
}
</style>
