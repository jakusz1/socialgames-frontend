<template>
  <div class="container">
    <div class="card-body">
      <div class="card-header">
        <h2>{{$t('start.new_game_title')}}</h2>
      </div>
      <div class="card-footer">
        <form @submit.prevent="startGame" class="form-inline">
          <select v-model="game_lang" class="form-control form-control-lg">
            <option v-for="(lang, i) in langs" :key="`Lang${i}`" :value="lang">{{ lang }}</option>
          </select>
          <button class="btn btn-success btn-lg">{{$t('start.btn')}}</button>
        </form>
      </div>
    </div>
    <div class="card-body">
      <div class="card-header">
        <h2>{{$t('controller.connect_title')}}</h2>
      </div>
      <div class="card-footer">
        <form @submit.prevent="startController" class="form-inline">
          <input pattern=".{4}" required :title="$t('code.length')" v-model="code" class="form-control form-control-lg" type="text" :placeholder="$t('controller.code')" />
          <button class="btn btn-success btn-lg">{{$t('controller.join')}}</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
const $ = window.jQuery

export default {
  data () {
    return {
      sessionStarted: false,
      mode: 'wait_for_start',
      players: [],
      answers: [],
      graph: null,
      game: {},
      kek: '',
      websocket: null,
      code: '',
      langs: ['pl_PL', 'en_US'],
      game_lang: 'pl_PL'
    }
  },

  created () {
    this.username = sessionStorage.getItem('username')

    // Setup headers for all requests
    $.ajaxSetup({
      headers: {
        'Authorization': `Token ${sessionStorage.getItem('authToken')}`
      }
    })
  },
  methods: {
    startGame () {
      window.jQuery.post('http://192.168.1.111:8000/api/games/', {lang: this.game_lang}, (data) => {
        this.$router.push(`/games/${data.uri}/`)
      })
        .fail((response) => {
          alert(response.responseText)
        })
    },
    startController () {
      this.$router.push(`/controllers/${this.code.toLowerCase()}/`)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
form input[type="text"] {
    text-transform: lowercase;
}
</style>
