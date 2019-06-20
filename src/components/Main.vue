<template>
  <div class="container my-auto">
    <div class="row">
      <div class="col">
    <div class="card text-white bg-primary mt-2">
      <div class="card-header text-left">
        <h3>{{$t('start.new_game_title')}}</h3>
      </div>
      <div class="card-body">
        <form @submit.prevent="startGame" class="form-group">
          <select v-model="game_lang" class="form-control form-control-lg">
            <option v-for="(lang, i) in langs" :key="`loc${i}`" :value="lang">{{$t("loc."+lang)}}</option>
          </select>
          <button class="btn btn-outline-light btn-lg btn-block mt-2">{{$t('start.btn')}}</button>
        </form>
      </div>
    </div>
      </div>
      <div class="col">
    <div class="card text-white bg-success mt-2">
      <div class="card-header text-left">
        <h3>{{$t('controller.connect_title')}}</h3>
      </div>
      <div class="card-body">
        <form @submit.prevent="startController" class="form-group">
          <input pattern=".{4}" required :title="$t('code.length')" v-model="code" class="form-control form-control-lg" type="text" :placeholder="$t('controller.code')" />
          <button class="btn btn-outline-light btn-lg btn-block mt-2">{{$t('controller.join')}}</button>
        </form>
      </div>
    </div>
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
      websocket: null,
      code: '',
      langs: ['en_US', 'pl_PL'],
      game_lang: 'en_US'
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
      window.jQuery.post(`http://${this.$backend}/api/games/`, {lang: this.game_lang}, (data) => {
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
