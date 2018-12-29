<template>
  <div class="d-flex flex-column flex-grow-1" v-if="sessionStarted">
    <div v-if="mode == 'game'" class="d-flex flex-grow-1">
      <TrendsGame v-bind:graph="graph" v-bind:answers="answers" ref="gameView" />
    </div>
    <div v-else-if="mode == 'wait_for_start'" class="card-body">
      <div class="card-header">{{ $t('waiting.title') }}</div>
    </div>
    <transition-group name="list-complete" tag="div" class="row">
      <div v-for="player in players" :key="player.id" class="col-sm">
        {{player.username}}
      </div>
    </transition-group>
  </div>
  <div v-else-if="!this.$route.params.uri" class="container">
    <div class="card-body">
      <div class="card-header">
        <h2>{{$t('start.new_game_title')}}</h2>
      </div>
      <div class="card-footer">
        <form @submit.prevent="startGameSession" class="form-inline">
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
import TrendsGame from './games/TrendsGame.vue'
const $ = window.jQuery

export default {
  components: {
    TrendsGame
  },
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
    if (this.$route.params.uri) {
      this.joinGameSession()
    }
  },
  methods: {
    startGameSession () {
      window.jQuery.post('http://localhost:8000/api/games/', {lang: this.game_lang}, (data) => {
        this.sessionStarted = true
        this.$router.push(`/games/${data.uri}/`)
        this.joinGameSession()
      })
        .fail((response) => {
          alert(response.responseText)
        })
    },
    joinGameSession () {
      const uri = this.$route.params.uri

      $.ajax({
        url: `http://localhost:8000/api/games/${uri}/`,
        data: {username: this.username},
        type: 'PATCH',
        success: (data) => {
          const user = data.game.players.find((player) => player.username === this.username)
          this.game = data.game
          this.players = data.game.players
          this.start_game(this.game)
          if (user) {
            this.sessionStarted = true
            this.connectToWebSocket()
          }
        }
      })
    },

    startController () {
      this.$router.push(`/controllers/${this.code.toLowerCase()}/`)
    },

    connectToWebSocket () {
      this.websocket = new WebSocket(`ws://localhost:8000/ws/games/${this.$route.params.uri}`)
      this.websocket.onopen = this.onOpen
      this.websocket.onclose = this.onClose
      this.websocket.onmessage = this.onMessage
      this.websocket.onerror = this.onError
    },

    onOpen (event) {
      console.log('Connection opened.', event.data)
    },

    onClose (event) {
      console.log('Connection closed.', event.data)
      setTimeout(this.connectToWebSocket, 5000)
    },

    onMessage (event) {
      debugger
      const data = JSON.parse(event.data)
      this[data.command](data.data)
    },

    start_game (data) {
      if (data.step === 'PRE') {
        this.mode = 'wait_for_start'
      } else {
        this.mode = 'game'
      }
    },

    results_graph (data) {
      debugger
      this.graph = JSON.parse(data)
      debugger
      // this.game = data.game
    },

    results_answers (data) {
      debugger
      this.answers = JSON.parse(data)
      debugger
    },

    all_answers (data) {
      this.$refs.gameView.nextScreen()
      debugger
    },

    update_players_list (data) {
      this.players = data.players
    },

    go_back (data) {
      this.websocket.close()
      this.sessionStarted = false
      this.$router.push(`/games/`)
    },

    onError (event) {
      alert('An error occured:', event.data)
    }
  }
  // watch: {
  //   mode: function (val) {
  //     if (val === 'game') {
  //       this.gameView = this.$children[0]
  //       debugger
  //     } else {
  //       this.gameView = null
  //     }
  //   }
  // }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
form input[type="text"] {
    text-transform: lowercase;
}
</style>
