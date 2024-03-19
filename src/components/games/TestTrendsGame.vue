/* eslint-disable */
<template>
  <div class="d-flex flex-grow-1 gt-hand">
      <screen>
        <score-table :key=0 :title="$t('score.round')" :players="players" />
      </screen>
  </div>
</template>

<script>
import GameView from './models/GameView.vue'
/* eslint-disable */
export default {
  mixins: [ GameView ],
  props: {
    answers: {default: () => [{player_id: 'aaa', username: 'first_gamer', text: 'buysaarobux', score: 230}, {player_id: 'aaa1', username: 'other_guy', text: 'free robux', score: 22}]},
    graph: {default: () => ({'columns': ['trump', 'biden'], 'index': [1654387200000, 1654992000000, 1655596800000, 1656201600000, 1656806400000, 1657411200000, 1658016000000, 1658620800000, 1659225600000, 1659830400000, 1660435200000, 1661040000000, 1661644800000, 1662249600000, 1662854400000, 1663459200000, 1664064000000, 1664668800000, 1665273600000, 1665878400000, 1666483200000, 1667088000000, 1667692800000, 1668297600000, 1668902400000, 1669507200000, 1670112000000, 1670716800000, 1671321600000, 1671926400000, 1672531200000, 1673136000000, 1673740800000, 1674345600000, 1674950400000, 1675555200000, 1676160000000, 1676764800000, 1677369600000, 1677974400000, 1678579200000, 1679184000000, 1679788800000, 1680393600000, 1680998400000, 1681603200000, 1682208000000, 1682812800000, 1683417600000, 1684022400000, 1684627200000], 'data': [[20, 18], [26, 23], [28, 31], [32, 17], [24, 22], [77, 33], [51, 33], [28, 20], [26, 18], [66, 18], [42, 16], [31, 38], [32, 30], [30, 16], [26, 14], [32, 19], [21, 16], [22, 22], [24, 19], [21, 17], [21, 15], [24, 18], [38, 16], [71, 18], [29, 17], [19, 13], [29, 13], [31, 11], [29, 9], [23, 9], [19, 10], [15, 19], [14, 15], [14, 12], [16, 12], [18, 24], [17, 14], [19, 17], [15, 13], [17, 13], [26, 14], [81, 11], [65, 15], [100, 14], [28, 13], [19, 14], [22, 21], [20, 16], [40, 17], [20, 13], [20, 12]]})},
    winners: {default: null}
  },
  data () {
    return {
      currentWord: 'no-data',
      options: {responsive: true, maintainAspectRatio: false},
      players: [{player_id: '11', username: 'first_gamer', score: 310, color: 2},
                {player_id: '22', username: 'other_guy', score: 221, color: 1},
                {player_id: '34', username: 'next_guy', score: 202, color: 0},
                {player_id: '54', username: 'best_gaymer', score: 42, color: 3},
                {player_id: '65', username: 'kox', score: 8, color: 4}
              ]
    }
  },
  methods: {}
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Indie+Flower|KoHo:600');
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
td {
  font-size: 7vh;
}
</style>
