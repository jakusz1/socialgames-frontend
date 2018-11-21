<script>
import { Line } from 'vue-chartjs'

export default {
  extends: Line,
  props: {
    chartdata: {default: null},
    options: {default: null}
  },
  data () {
    return {
      isScreen: false,
      isChart: true
    }
  },
  mounted () {
    this.renderChart(this.chartdata, this.options)
    // labels: ['January', 'February'],
    // datasets: [
    //   {
    //     label: 'Data One',
    //     backgroundColor: '#f87979',
    //     data: [40, 20]
    //   }
    // ]},
    // {
    //   responsive: true
    // })
  }
}
</script>

<style>
</style>
