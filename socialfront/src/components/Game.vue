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
        {{player.username}} {{player.score}}
      </div>
    </transition-group>
  </div>
  <div v-else-if="!this.$route.params.uri">
    <button @click="startGameSession" class="btn btn-primary btn-lg btn-block">{{$t('start.game')}}</button>
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
      websocket: null
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
      window.jQuery.post('http://localhost:8000/api/games/', {}, (data) => {
        this.sessionStarted = true
        this.$router.push(`/games/${data.uri}/`)
        this.joinGameSession()
      })
        .fail((response) => {
          alert(response.responseText)
        })
    },
    postMessage (event) {
      const data = {message: this.message}

      window.jQuery.post(`http://localhost:8000/api/games/${this.$route.params.uri}/messages/`, data, (data) => {
        this.message = '' // clear the message after sending
      })
        .fail((response) => {
          alert(response.responseText)
        })
    },
    testM () {
      debugger
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
          debugger
          this.players = data.game.players
          if (this.game.step === 'PRE') {
            this.mode = 'wait_for_start'
          } else {
            this.mode = 'game'
          }
          if (user) {
            // The user belongs/has joined the session
            this.sessionStarted = true
            this.connectToWebSocket()
          }
        }
      })
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

      // Try and Reconnect after five seconds
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
</style>
