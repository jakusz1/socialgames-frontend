<template>
  <div class="d-flex">
    <div class="m-4" v-bind:key="answer.id" v-for="answer in answers">
      <h3>{{answer.text}} {{answer.score}}</h3>
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

<style scoped>
.m-4:nth-of-type(1) h3{
  color: '#007bff';
}
.m-4:nth-of-type(2) h3{
  color: '#6f42c1';
}
.m-4:nth-of-type(3) h3{
  color: '#fd7e14';
}
.m-4:nth-of-type(4) h3{
  color: '#28a745';
}
.m-4:nth-of-type(5) h3{
  color: '#17a2b8';
}
</style>
