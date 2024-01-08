<template>
  <div class="d-flex flex-column">
    <div class="d-flex m-4 answer flex-row align-items-center" v-bind:key="answer.player_id" v-for="(answer, index) in answers">
      <div class="d-flex flex-column flex-grow-1" style="text-align: left"><h2 style="font-style: italic">{{answer.text}}</h2><h3 v-bind:style="{ color: player_colors[index] }">{{answer.username}}</h3></div>
      <div style="margin-left: 1em;"><h1>+{{answer.score}}</h1></div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
export default {
  name: 'AnswerList',
  props: {
    answers: {default: null}
  },
  data () {
    return {
      isScreen: false,
      isChart: false,
      isAnswerList: true,
      player_colors: Vue.prototype.$colors
    }
  }
}
</script>

<style>

</style>
