<template>
  <div class="container">
    <div v-if="sessionStarted">
      <div class="row">
        <div v-for="player in players" :key="player.id" class="col-sm">
          {{player.username}} {{player.score}}
        </div>
      </div>
      <div v-if="mode == 'game'">
        <TrendsGame :embedded="true" :keyboardNavigation="false" :mouseNavigation="false"></TrendsGame>
      </div>
      <div v-else-if="mode == 'wait_for_start'" class="card-body">
        <div class="card-header">{{ $t('waiting.title') }}</div>
      </div>
    </div>
    <div v-else>
      <button @click="startGameSession" class="btn btn-primary btn-lg btn-block">{{$t('start.game')}}</button>
    </div>
  </div>
</template>

<script>
import TrendsGame from './games/TrendsGame'
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
      game: {}
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
      $.post('http://localhost:8000/api/games/', {game_type: 'tre'}, (data) => {
        alert("A new session has been created you'll be redirected automatically")
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

      $.post(`http://localhost:8000/api/games/${this.$route.params.uri}/messages/`, data, (data) => {
        this.message = '' // clear the message after sending
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
          debugger
          this.players = data.game.players
          if (this.game.started) {
            this.mode = 'game'
          } else {
            this.mode = 'wait_for_start'
          }
          if (user) {
            // The user belongs/has joined the session
            this.sessionStarted = true
            this.connectToWebSocket()
          }
        }
      })
    },

    fetchGameSessionHistory () {
      $.get(`http://127.0.0.1:8000/api/games/${this.$route.params.uri}/messages/`, (data) => {
        this.messages = data.messages
      })
    },
    connectToWebSocket () {
      const websocket = new WebSocket(`ws://localhost:8000/ws/games/${this.$route.params.uri}`)
      websocket.onopen = this.onOpen
      websocket.onclose = this.onClose
      websocket.onmessage = this.onMessage
      websocket.onerror = this.onError
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
      this.mode = data.started ? 'game' : 'wait_for_start'
    },

    new_player_joined (data) {
      this.players = data.players
    },

    onError (event) {
      alert('An error occured:', event.data)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
