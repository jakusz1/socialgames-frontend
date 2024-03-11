<template>
  <div class="d-flex flex-column flex-grow-1">
    <div class="d-flex flex-grow-1">
      <TestTrendsGame ref="gameView" />
    </div>
    <transition-group name="flip-list" tag="div" class="row">
      <div v-for="(player, index) in players" :key="player.id" class="col-sm text-5">
        <h1 v-bind:style="{ color: $colors[index] }">{{player.username}}</h1>
      </div>
      <div :key=111111 class="ml-auto align-self-center">
        <button type="button" class="btn btn-outline-secondary btn-lg" @click='pause_step()'>►❚❚</button>
        <button type="button" style="margin-right: 1vw;" class="btn btn-outline-secondary btn-lg" @click='skip_current_step()'>►►</button>
      </div>
    </transition-group>
  </div>
</template>

<script>
import TestTrendsGame from './games/TestTrendsGame.vue'
import TrendsGame from './games/TrendsGame.vue'
const $ = window.jQuery

export default {
  components: {
    TrendsGame,
    TestTrendsGame
  },
  data () {
    return {
      sessionStarted: true,
      mode: 'wait_for_start',
      players: [{id: 1, username: 'first_gamer'}, {id: 2, username: 'other_guy'}],
      new_players: [],
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
    $.ajaxSetup({
      headers: {
        'Authorization': `Token ${sessionStorage.getItem('authToken')}`
      }
    })
    this.joinGameSession()
  },
  methods: {
    joinGameSession () {
      const uri = this.$route.params.uri

      $.ajax({
        url: `http://${this.$backend}/api/games/${uri}/`,
        data: {username: this.username},
        type: 'PATCH',
        success: (data) => {
          const user = data.game.players.find((player) => player.username === this.username)
          this.game = data.game
          this.players = data.game.players
          this.start_game(this.game)
          if (user) {
            this.connectToWebSocket()
          }
        }
      })
    },

    connectToWebSocket () {
      this.websocket = new WebSocket(`ws://${this.$backend}/ws/games/${this.$route.params.uri}`)
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
      const data = JSON.parse(event.data)
      this[data.command](data.data)
    },

    start_game (data) {
      if (data.status === 'PRE') {
        this.mode = 'wait_for_start'
      } else {
        this.mode = 'game'
      }
    },

    results_graph (data) {
      this.graph = JSON.parse(data)
    },

    results_answers (data) {
      this.answers = JSON.parse(data)
    },

    all_answers (data) {
      this.$refs.gameView.nextScreen()
    },

    update_players_list (data) {
      this.players = data.players
    },

    send_players_silent (data) {
      this.new_players = data.players
    },

    update_new_players (data) {
      this.players = this.new_players
    },

    go_back (data) {
      this.$router.push(`/`)
    },

    onError (event) {
      alert('An error occured:', event.data)
    },

    skip_current_step () {
      this.$refs.gameView.currentScreen.forward()
      alert('essa')
    },

    pause_step () {
      this.$refs.gameView.currentScreen.switch_pause()
    }
  }
}
</script>

<style scoped>
form input[type="text"] {
    text-transform: lowercase;
}
.text-5{
  font-size: 5vh;
}
@import url('https://fonts.googleapis.com/css?family=Indie+Flower|KoHo:600');
div {
  font-family: 'KoHo', sans-serif;
}
</style>
