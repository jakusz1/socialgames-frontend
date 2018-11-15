<template>
  <div class="screen" v-if="active">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'Screen',
  props: {
    duration: {default: 0},
    onEndFun: {default: () => function () { }}
  },
  data: function () {
    return {
      active: false,
      isScreen: true,
      screenTimer: 0
    }
  },
  watch: {
    step: function (val) {
      this.$parent.step = val
    },
    active: function (val) {
      var self = this
      if (val) {
        this.screenTimer = 0
        this.timerUpdater = setInterval(function () {
          self.screenTimer++
        }, 1000)
      } else {
        clearInterval(this.timerUpdater)
      }
    },
    screenTimer: function (val) {
      if (this.duration !== 0 && val >= this.duration) {
        this.onEndFun()
        this.$parent.nextScreen()
      }
    }
  }
}
</script>
