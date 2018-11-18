<template>
<transition name="fade" mode="out-in">
  <transition-group name="flip-list" tag="div" class="d-flex flex-grow-1 justify-content-center align-items-center flex-column screen" v-if="active">
    <slot></slot>
  </transition-group>
</transition>
</template>

<script>
export default {
  props: {
    duration: {default: 0},
    onStartFun: {default: () => function () { }},
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
        this.onStartFun()
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

<style scoped>
.screen {
  position: absolute;
  width: 100vw;
  height: 85vh;
}
</style>
