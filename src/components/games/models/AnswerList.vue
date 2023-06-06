<template>
  <div class="d-flex">
    <div class="m-4 answer" v-bind:key="answer.player_id" v-for="answer in answers">
      <h3>{{answer.username}}</h3><h3>{{answer.text}} {{answer.score}}</h3>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AnswerList',
  props: {
    answers: {default: null}
  },
  data () {
    return {
      isScreen: false,
      isChart: false,
      isAnswerList: true
    }
  }
}
</script>

<style>

</style>
