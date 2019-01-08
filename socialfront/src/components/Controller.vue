<template>
  <div class="container">
    <div v-if="sessionStarted">
      <div v-if="mode == 'blank'" class="card-body">
      </div>
      <div v-else-if="mode == 'wait_for_start'" class="card-body">
        <button @click="startGame" :disabled="players.length < 2" class="btn btn-primary btn-block">{{$t('start.game')}}</button>
        <div class="card-footer">
        <h2>{{$t('waiting.players')}}</h2>
        <div v-for="player in players" :key="player.id" class="col-sm">
          <a data-toggle="tooltip" data-html="true" :title="'<p><b>'+player.email+'</b></p><p>'+$t('total.score')+': '+player.total_score+'</p><p>'+$t('total.won')+': '+player.total_won+'</p>'" data-placement="bottom">{{player.username}}</a>
        </div>
        </div>
      </div>
      <div v-else-if="mode == 'textLR' && title" class="card-body">
        <div class="card-header">{{ title }}</div>
        <div class="card-footer">
        <form v-on:submit.prevent>
              <input :maxlength="20" v-model="message" type="text" :placeholder="$t('type.ans')" class="p-2 w-100" />
              <button class="btn btn-outline-secondary m-2" v-on:click="postAnsL(true)" :disabled="this.message.length==0">{{$t('send')}}: {{message}} {{title}}</button>
              <button class="btn btn-outline-secondary m-2" v-on:click="postAnsL(false)" :disabled="this.message.length==0">{{$t('send')}}: {{title}} {{message}}</button>
        </form>
        </div>
      </div>
      <div v-else-if="mode == 'textLR'" class="card-body">
        <div class="card-header">{{ $t('inprog') }}</div>
      </div>
    </div>
  </div>
</template>

<script>
const $ = window.jQuery

$('body').tooltip({
  selector: '[data-toggle="tooltip"]'
})

export default {
  data () {
    return {
      sessionStarted: false,
      mode: 'blank',
      messages: [],
      title: '',
      message: '',
      round_id: null,
      gameType: '',
      game: '',
      players: []
    }
  },

  created () {
    this.username = sessionStorage.getItem('username')
    $.ajaxSetup({
      headers: {
        'Authorization': `Token ${sessionStorage.getItem('authToken')}`
      }
    })
    if (this.$route.params.uri) {
      this.joinGameSession()
      this.connectToWebSocket()
    }
  },

  methods: {
    postAnsL (left) {
      var data = ''
      if (left) {
        data = {'text': this.message + ' ' + this.title,
          'type': 'default'}
      } else {
        data = {'text': this.title + ' ' + this.message,
          'type': 'default'}
      }
      $.post(`http://${this.$backend}/api/rounds/${this.round_id}/answers/`, data, (data) => {
        this.mode = 'blank'
      })
        .fail((response) => {
          alert(response.responseText)
        })
      this.message = ''
    },
    joinGameSession () {
      const uri = this.$route.params.uri

      $.ajax({
        url: `http://${this.$backend}/api/games/${uri}/`,
        data: {username: this.username},
        type: 'PATCH',
        success: (data) => {
          const user = data.game.players.find((player) => player.username === this.username)
          this.game = data.game
          if (this.game.status === 'PRE') {
            this.mode = 'wait_for_start'
          } else if (this.game.status === 'ANS') {
            this.mode = 'textLR'
          } else {
            this.mode = 'blank'
          }
          if (user) {
            this.sessionStarted = true
          }
        }
      })
    },

    startGame () {
      const uri = this.$route.params.uri
      $.ajax({
        url: `http://${this.$backend}/api/games/${uri}/start`,
        data: {username: this.username},
        type: 'PATCH',
        success: (data) => {
          this.game = data.game
          if (this.game.status === 'PRE') {
            this.mode = 'wait_for_start'
          } else if (this.game.status === 'ANS') {
            this.mode = 'textLR'
          } else {
            this.mode = 'blank'
          }
        }
      })
    },

    connectToWebSocket () {
      const websocket = new WebSocket(`ws://${this.$backend}/ws/controllers/${this.$route.params.uri}`)
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
      setTimeout(this.connectToWebSocket, 5000)
    },

    onMessage (event) {
      const data = JSON.parse(event.data)
      this[data.command](data.data)
    },

    start_game (data) {
      if (data.status === 'PRE') {
        this.mode = 'wait_for_start'
      } else if (data.status === 'ANS') {
        this.mode = 'textLR'
      } else {
        this.mode = 'blank'
      }
    },

    new_round (data) {
      this.mode = 'textLR'
      this.title = data.word
      this.round_id = data.id
    },

    update_players_list (data) {
      this.players = data.players
      $('[data-toggle="tooltip"]').tooltip()
    },

    go_back (data) {
      this.$router.push(`/`)
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
