<script>
import Screen from './Screen.vue'

export default {
  name: 'GameView',
  components: {
    Screen
  },
  data: function () {
    return {
      currentScreenIndex: 1,
      currentScreen: null,
      screenTimer: 0,
      screens: [],
      active: true
    }
  },
  mounted: function () {
    this.findScreens()
    this.timerUpdater = setInterval(function () {
      self.slideTimer++
    }, 1000)
  },
  beforeDestroy: function () {
    clearInterval(this.timerUpdater)
  },
  methods: {
    findScreens: function () {
      var self = this
      this.$children.forEach(function (el) {
        self.screens.push(el)
      })
      if (self.screens) {
        this.currentScreen = self.screens[0]
      }
    },
    nextScreen: function () {
      if (this.currentScreenIndex < this.screens.length + 1) {
        this.currentScreenIndex++
      }
    }
  },
  watch: {
    currentScreen: function (newScreen, oldScreen) {
      debugger
      if (oldScreen) {
        oldScreen.active = false
      }
      this.screenTimer = 0
      newScreen.active = true
    },
    currentScreenIndex: function (index) {
      this.currentScreen = this.screens[index - 1]
    }
  }
}
</script>
