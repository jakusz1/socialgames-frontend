<template>
  <div class="container">
    <div v-if="sessionStarted">
      <div v-if="mode == 'blank'" class="card-body">
      </div>
      <div v-else-if="mode == 'wait_for_start'" class="card-body">
        <button @click="startGame" class="btn btn-primary">{{$t('start.game')}}</button>
      </div>

      <div v-else-if="mode == 'text'" class="card-body">
        <div class="card-header">{{ title }}</div>
        <div class="card-footer">
        <form @submit.prevent="postMessage">
              <input :maxlength="20" v-model="message" type="text" :placeholder="$t('type.ans')" class="p-2 w-100" />
              <button class="btn btn-outline-secondary w-100 m-2">{{$t('send')}}: {{message}}</button>
        </form>
        </div>
      </div>

      <div v-else-if="mode == 'textLR'" class="card-body">
        <div class="card-header">{{ title }}</div>
        <div class="card-footer">
        <form>
              <input :maxlength="20" v-model="message" type="text" :placeholder="$t('type.ans')" class="p-2 w-100" />
              <button class="btn btn-outline-secondary m-2" v-on:click="postAnsL(true)">{{$t('send')}}: {{message}} {{title}}</button>
              <button class="btn btn-outline-secondary m-2" v-on:click="postAnsL(false)">{{$t('send')}}: {{title}} {{message}}</button>
        </form>
        </div>
      </div>

      <div v-else-if="mode == 'choiceText'" class="card-body">
        <div class="card-header">{{ title }}</div>
        <div class="card-footer">
          <div v-for="choice in choices" :key="choice.id">
            <button class="btn btn-outline-secondary w-100 m-2 p-2" v-on:click="postChoice(choice.id)">{{choice.text}}</button>
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
      mode: 'blank',
      messages: [],
      title: '',
      message: '',
      task_id: null,
      gameType: '',
      game: '',
      choices: [{'id': 'heh', 'text': 'Sample answer number one'},
        {'id': 'heh2', 'text': 'Sample answer number two'}]
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
      this.connectToWebSocket()
    }
  },

  methods: {
    postMessage (event) {
      const data = {message: this.message}

      $.post(`http://localhost:8000/api/games/${this.$route.params.uri}/messages/`, data, (data) => {
        this.message = '' // clear the message after sending
      })
        .fail((response) => {
          alert(response.responseText)
        })
    },
    postChoice (choice) {
      const data = {message: choice}

      $.post(`http://localhost:8000/api/games/${this.$route.params.uri}/messages/`, data, (data) => {
        this.mode = 'blank'
      })
        .fail((response) => {
          alert(response.responseText)
        })
    },
    postAnsL (left) {
      var data = ''
      if (left) {
        data = {'text': this.message + ' ' + this.title,
          'type': 'default'}
      } else {
        data = {'text': this.title + ' ' + this.message,
          'type': 'default'}
      }
      $.post(`http://localhost:8000/api/tasks/${this.task_id}/answers/`, data, (data) => {
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
        url: `http://localhost:8000/api/games/${uri}/`,
        data: {username: this.username},
        type: 'PATCH',
        success: (data) => {
          const user = data.game.players.find((player) => player.username === this.username)
          this.game = data.game
          if (this.game.started) {
            this.mode = 'blank'
          } else {
            this.mode = 'wait_for_start'
          }
          if (user) {
            // The user belongs/has joined the session
            this.sessionStarted = true
            // this.fetchGameSessionHistory()
          }
        }
      })
    },

    startGame () {
      const uri = this.$route.params.uri
      $.ajax({
        url: `http://localhost:8000/api/games/${uri}/start`,
        data: {username: this.username},
        type: 'PATCH',
        success: (data) => {
          this.game = data.game
          if (this.game.started) {
            this.mode = 'blank'
          } else {
            this.mode = 'wait_for_start'
          }
        }
      })
    },

    connectToWebSocket () {
      const websocket = new WebSocket(`ws://localhost:8000/ws/controllers/${this.$route.params.uri}`)
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
      this.mode = data.started ? 'blank' : 'wait_for_start'
    },

    new_trends_word (data) {
      this.mode = 'textLR'
      this.title = data.word
      this.task_id = data.id
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
