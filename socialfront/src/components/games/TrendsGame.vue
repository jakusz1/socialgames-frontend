<template>
  <div class="d-flex flex-grow-1">
    <Screen :duration="5">
      <h1>Ja pierdole</h1>
    </Screen>
    <Screen>
      <h1>Co do kurwy</h1>
    </Screen>
  </div>
</template>

<script>
import GameView from './models/GameView.vue'

export default {
  mixins: [ GameView ],
  data () {
    return {
      kek: ''
    }
  },
  methods: {
    testMethod () {
      debugger
      console.log('CHUUUUUUUUUUUUUUUUJ')
      this.kek = 'CHUJ PIZDA DZIALA'
      this.$parent.kek = 'CHUJ PIZDA DZIALA'
      this.$parent.$parent.kek = 'CHUJ PIZDA DZIALA'
    }
  }
}
</script>

<style scoped>
</style>
