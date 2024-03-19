<template>
  <div :key=0>
    <h2>{{ title }}</h2>
    <table class="table">
      <tbody>
        <tr v-for="(player, pos) in players" :key="pos">
          <template>
            <td>{{pos+1}}.</td>
            <td style="text-align: left" v-bind:style="{ color: $colors[player.color], opacity: isVisible(pos) ? 1 : 0 }">{{player.username}}</td>
            <td style="text-align: right" v-bind:style="{ opacity: isVisible(pos) ? 1 : 0 }">{{player.score}}</td>
          </template>
        </tr>
      </tbody>
    </table>
</div>
</template>

<script>
export default {
  props: {
    title: { default: 0 },
    players: { default: [] }
  },
  methods: {
    isVisible (pos) {
      return (this.players.length - pos) <= this.$parent.$parent.screenTimer
    }
  }
}
</script>

<style scoped>
h2 {
  font-size: 12vh;
}
td {
  font-size: 7vh;
}
</style>
