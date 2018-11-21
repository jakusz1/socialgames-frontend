<template>
  <div class="d-flex">
    <div class="m-4" v-bind:key="answer.id" v-for="answer in answers">
      <h4>{{answer.username}}</h4><h3>{{answer.text}} {{answer.score}}</h3>
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
