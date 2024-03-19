<script>
import Screen from './Screen.vue'
import Chart from './Chart.vue'
import AnswerList from './AnswerList.vue'
import ScoreTable from './ScoreTable.vue'

export default {
  name: 'GameView',
  components: {
    Screen,
    Chart,
    'answerlist': AnswerList,
    ScoreTable
  },
  data: function () {
    return {
      currentScreenIndex: 1,
      currentScreen: null,
      screens: [],
      chart: null,
      charts: [],
      active: true
    }
  },
  mounted: function () {
    this.findChildren()
  },
  beforeDestroy: function () {
    clearInterval(this.timerUpdater)
  },
  methods: {
    findChildren: function () {
      var self = this
      this.$children.forEach(function (el) {
        if (el.isScreen) {
          self.screens.push(el)
        } else if (el.isChart) {
          self.charts.push(el)
        }
      })
      if (self.screens) {
        this.currentScreen = self.screens[0]
      }
    },
    updateCharts (data) {
      this.charts.forEach(function (chart) {
        chart.chartdata = data
        chart.options = {
          responsive: true,
          maintainAspectRatio: false }
      })
    },
    nextScreen: function () {
      if (this.currentScreenIndex < this.screens.length + 1) {
        this.currentScreenIndex++
      }
    },
    between: function (from = 0, to = Number.MAX_VALUE) {
      return this.currentScreen && this.currentScreen.screenTimer >= from && this.currentScreen.screenTimer <= to
    },
    timer: function () {
      if (this.currentScreen) {
        return this.currentScreen.screenTimer
      } else {
        return 0
      }
    }
  },
  watch: {
    currentScreen: function (newScreen, oldScreen) {
      if (oldScreen) {
        oldScreen.active = false
      }
      this.screenTimer = 0
      newScreen.active = true
    },
    currentScreenIndex: function (index) {
      this.currentScreen = this.screens[index - 1]
    },
    charts: function (val) {
      this.updateCharts(val)
    }
  }
}
</script>
