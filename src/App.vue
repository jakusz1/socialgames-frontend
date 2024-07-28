<template>
  <div id="app" class="d-flex flex-column flex-grow-1">
    <nav class="navbar navbar-light bg-light">
      <a class="navbar-brand mr-auto" href="#/">
        <img src="@/assets/logo.png" width="45" height="30" class="d-inline-block align-top" alt="">
        {{$t('app.name')}}
      </a>
      <a v-if="getToken()" class="btn btn-link my-2 my-sm-0" href="#/profile">⬢ {{getUsername()}}</a>
      <LocaleChanger/>
      <a v-if="getToken()" class="btn btn-outline-success my-2 my-sm-0" href="#/logout">{{$t('log.out')}}</a>
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
  data () {
    return {
      username: ''
    }
  },
  methods: {
    getToken () {
      return sessionStorage.getItem('authToken')
    },
    getUsername () {
      return sessionStorage.getItem('username')
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Indie+Flower|KoHo:600');
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: inherit;
}
.card .card-header {
  font-size: 1.5rem
}
</style>
