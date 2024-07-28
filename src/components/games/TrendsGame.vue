<!-- eslint-disable vue/no-v-for-template-key -->
<template>
  <div class="d-flex flex-grow-1 gt-hand">
    <screen :duration="5">
      <h1 :key=0>{{$t('tre.title')}}</h1>
      <h4 :key=1 v-if="between(2,5)">{{$t('tre.subtitle')}}</h4>
    </screen>
    <screen :duration="10">
      <h2 :key=0>{{$t('tre.howto.title')}}</h2>
      <h4 :key=1 v-if="between(2,10)">{{$t('tre.howto.text')}}</h4>
    </screen>
    <template v-for="(item, multiplier) in 3">
      <screen :key="`${multiplier}start`" :duration="6">
          <h2 :key=0>{{ $t('tre.round') }} {{ multiplier + 1 }}</h2>
          <h3 :key=1 v-if="between(2,6) & multiplier>0">{{ $t(`tre.multiplier${multiplier}`) }}</h3>
        </screen>
      <template v-for="(item2, index) in 3">
        <screen :key="`${multiplier}${index}1`" :duration="8" :onEndFun="getWord">
          <h3 :key=0>{{ $t('tre.rd4q', [index+1]) }}</h3>
          <h1 :key=1 v-if="between(2,8)">{{ 7-timer() }}</h1>
        </screen>
        <screen :key="`${multiplier}${index}2`" :duration="61">
          <h2 :key=0>{{currentWord}}</h2>
          <h1 :key=1 v-if="between(1,61)">{{ 60-timer() }}</h1>
          <h4 :key=2 v-if="between(5,26)">{{ $t('type_dev') }}</h4>
          <h4 :key=3 v-if="between(51,61)">{{ $t('hurry') }}</h4>
        </screen>
        <screen :key="`${multiplier}${index}3`" :duration="3" :onStartFun="endRound">
          <h2 :key=0>{{ $t('endans') }}</h2>
        </screen>
        <screen :key="`${multiplier}${index}4`" :duration="20" :onStartFun="update_new_players">
          <div :key=0 class="d-flex">
            <transition-group name="fade" tag="div" class="d-flex flex-grow-1 align-items-center">
              <div :key=1 class="chart-container flex-grow-1">
                <chart v-if="graph" v-bind:chartdata="graph" v-bind:options="options"></chart>
              </div>
              <div :key=2 v-if="between(2,)" class="d-flex">
                <answerlist v-if="answers" v-bind:answers="answers"></answerlist>
              </div>
            </transition-group>
          </div>
        </screen>
      </template>
      <screen v-if="multiplier<2" :key="`${multiplier}score`" :duration="10">
        <score-table :key=0 :title="$t('score.round')" :players="players" />
      </screen>
    </template>
    <screen :duration="20" :onStartFun="endGame" :onEndFun="go_back">
      <score-table :key=0 v-if="winners" :title="$t('score.final')" :players="winners" />
    </screen>
  </div>
</template>

<script>
import GameView from './models/GameView.vue'
const $ = window.jQuery

export default {
  mixins: [GameView],
  props: {
    answers: { default: [] },
    graph: { default: null }
  },
  data () {
    return {
      currentWord: 'no-data',
      options: { responsive: true, maintainAspectRatio: false },
      winners: [],
      players: []
    }
  },
  methods: {
    getWord () {
      $.get(`http://${this.$backend}/api/games/${this.$route.params.uri}/round`, (data) => {
        this.currentWord = data.text
      }).fail((response) => { alert(response.responseText) })
    },
    endRound () {
      $.ajax({
        url: `http://${this.$backend}/api/games/${this.$route.params.uri}/round`,
        type: 'DELETE',
        success: (data) => { this.players = data.players }
      })
    },
    endGame () {
      $.ajax({
        url: `http://${this.$backend}/api/games/${this.$route.params.uri}/`,
        type: 'DELETE',
        success: (data) => { this.winners = data.winners }
      })
    },
    go_back () {
      this.$parent.go_back()
    },
    update_new_players () {
      this.$parent.update_new_players()
    }
  }
}
</script>

<style scoped>
h1 {
  font-size: 16vh;
}
h2 {
  font-size: 12vh;
}
h3 {
  font-size: 7vh;
}
h4 {
  font-size: 5vh;
}
h5 {
  font-size: 3vh;
}
.gt-hand {
  font-family: 'KoHo', sans-serif;
}
.chart-container {
  width: 70vw;
}
</style>
