<template>
  <div class="d-flex flex-grow-1 gt-hand">
    <!-- <screen :duration="5">
      <h1 key="0">{{$t('tre.title')}}</h1>
      <h4 key="1" v-if="between(2,5)">{{$t('tre.subtitle')}}</h4>
    </screen>
    <screen :duration="5">
      <h2 key="0">{{$t('tre.howto.title')}}</h2>
      <h4 key="1" v-if="between(2,5)">{{$t('tre.howto.text')}}</h4>
    </screen> -->
    <template v-for="(item, index) in 3">
      <screen :key="index*10+1" :duration="8" :onEndFun="getWord">
        <h3 key="0">{{ $t('tre.rd4q', [index+1]) }}</h3>
        <h1 key="1" v-if="between(2,8)">{{ 7-timer() }}</h1>
      </screen>
      <screen :key="index*10+2" :duration="61">
        <h2 key="0">{{currentWord}}</h2>
        <h1 key="1" v-if="between(1,61)">{{ 60-timer() }}</h1>
        <h4 key="2" v-if="between(5,26)">{{ $t('type_dev') }}</h4>
        <h4 key="2" v-if="between(51,61)">{{ $t('hurry') }}</h4>
      </screen>
      <screen :key="index*10+3" :duration="5" :onStartFun="endTask">
        <h2 key="0">{{ $t('endans') }}</h2>
      </screen>
      <screen :key="index*10+4" :duration="61">
        <div key="0.1"><answerlist v-if="answers" v-bind:answers="answers"></answerlist></div>
        <div key="0.0"><chart v-if="graph" v-bind:chartdata="graph"></chart></div>
      </screen>
    </template>
  </div>
</template>

<script>
import GameView from './models/GameView.vue'
const $ = window.jQuery

export default {
  mixins: [ GameView ],
  props: {
    answers: {default: []},
    graph: {default: null}
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
    testMethod () {
      debugger
      console.log('CHUUUUUUUUUUUUUUUUJ')
      this.kek = 'CHUJ PIZDA DZIALA'
      this.$parent.kek = 'CHUJ PIZDA DZIALA'
      this.$parent.$parent.kek = 'CHUJ PIZDA DZIALA'
    },
    getWord () {
      $.get(`http://localhost:8000/api/games/${this.$route.params.uri}/task`, (data) => {
        this.currentWord = data.text
      })
        .fail((response) => {
          alert(response.responseText)
        })
    },
    endTask () {
      // $.delete(`http://localhost:8000/api/games/${this.$route.params.uri}/task`)
      //   .fail((response) => {
      //     alert(response.responseText)
      //   })
      $.ajax({
        url: `http://localhost:8000/api/games/${this.$route.params.uri}/task`,
        type: 'DELETE',
        success: () => {}
      })
    }
    // startGame () {
    //   debugger
    //   this.$parent.websocket.send(JSON.stringify({
    //     'command': 'start_game'
    //   }))
    //   debugger
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
