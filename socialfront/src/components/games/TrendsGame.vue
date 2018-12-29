<template>
  <div class="d-flex flex-grow-1 gt-hand">
    <screen :duration="5">
      <h1 key="0">{{$t('tre.title')}}</h1>
      <h4 key="1" v-if="between(2,5)">{{$t('tre.subtitle')}}</h4>
    </screen>
    <screen :duration="5">
      <h2 key="0">{{$t('tre.howto.title')}}</h2>
      <h4 key="1" v-if="between(2,5)">{{$t('tre.howto.text')}}</h4>
    </screen>
    <template v-for="(item, index) in 3">
      <screen :key="index*10+1" :duration="8" :onEndFun="getWord">
        <h3 key="0">{{ $t('tre.rd4q', [index+1]) }}</h3>
        <h1 key="1" v-if="between(2,8)">{{ 7-timer() }}</h1>
      </screen>
      <screen :key="index*10+2" :duration="61">
        <h2 key="0">{{currentWord}}</h2>
        <h1 key="1" v-if="between(1,61)">{{ 60-timer() }}</h1>
        <h4 key="2" v-if="between(5,26)">{{ $t('type_dev') }}</h4>
        <h4 key="3" v-if="between(51,61)">{{ $t('hurry') }}</h4>
      </screen>
      <screen :key="index*10+3" :duration="5" :onStartFun="endRound">
        <h2 key="0">{{ $t('endans') }}</h2>
      </screen>
      <screen :key="index*10+4" :duration="5">
        <div key="0.1"><answerlist v-if="answers" v-bind:answers="answers"></answerlist></div>
        <div key="0.0"><chart v-if="graph" v-bind:chartdata="graph"></chart></div>
      </screen>
    </template>
    <screen :duration="20" :onStartFun="endGame" :onEndFun="go_back">
      <h2 key="0" v-if="winners">{{winners[0].username}} {{$t('winner')}}</h2>
      <h1 key="1" v-if="winners">{{winners[0].score}}</h1>
      <h5 key="2" v-if="winners[1]">2. {{winners[1].username}} {{winners[1].username}}</h5>
      <h5 key="3" v-if="winners[2]">3. {{winners[2].username}} {{winners[2].username}}</h5>
    </screen>
  </div>
</template>

<script>
import GameView from './models/GameView.vue'
const $ = window.jQuery

export default {
  mixins: [ GameView ],
  props: {
    answers: {default: []},
    graph: {default: null},
    winners: {default: []}
  },
  data () {
    return {
      currentWord: 'no-data'
      // answers: [{'id': 1,
      //   'player': {'username': 'rikitiki'},
      //   'text': 'HASDJHASKJDH'}]
    }
  },
  methods: {
    getWord () {
      $.get(`http://localhost:8000/api/games/${this.$route.params.uri}/round`, (data) => {
        this.currentWord = data.text
      })
        .fail((response) => {
          alert(response.responseText)
        })
    },
    endRound () {
      $.ajax({
        url: `http://localhost:8000/api/games/${this.$route.params.uri}/round`,
        type: 'DELETE',
        success: () => {}
      })
    },
    endGame () {
      // this.$parent.username
      
      $.ajax({
        url: `http://localhost:8000/api/games/${this.$route.params.uri}/`,
        type: 'DELETE',
        data: {username: this.$parent.username},
        success: (data) => { this.winners = data.winners }
      })
    },
    go_back () {
      debugger
      this.$parent.go_back()
    }
    // startGame () {
    //   
    //   this.$parent.websocket.send(JSON.stringify({
    //     'command': 'start_game'
    //   }))
    //   
    // }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Indie+Flower|KoHo:600');
h1 {
  font-size: 16vh;
}
h2 {
  font-size: 12vh;
}
h3 {
  font-size: 8vh;
}
h4 {
  font-size: 4vh;
}
h5 {
  font-size: 3vh;
}
.gt-hand {
  font-family: 'KoHo', sans-serif;
}
</style>
