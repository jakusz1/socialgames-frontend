<script>
/* eslint-disable */
import { Line } from 'vue-chartjs'
import moment from 'moment'
import Vue from 'vue'


export default {
  extends: Line,
  props: {
    chartdata: { default: null },
    options: { default: null },
    cssClasses: { default: "chart"}
  },
  data() {
    return {
      isScreen: false,
      isChart: true
    }
  },
  mounted() {

    if (this.chartdata && typeof this.chartdata.columns !== 'undefined') {
      this.noData = false;
      const data = this.chartdata;
      const playersCount = data.columns.length;
      const datasets = prepareDatasets(data, playersCount);
      const labels = data.index;
      const x = {
        labels: labels,
        datasets: datasets
      }
      this.renderChart(x, {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
            padding: {
                right: 30,
            }
        },
        scales: {
          xAxes: [{
            type: 'time',
            time: {
                    unit: 'quarter'
                },
            ticks: {
              fontSize: 25,
              fontFamily: 'KoHo',
            },
            gridLines: {
              display: false
            }
          }],
          yAxes: [{
            display: false,
            gridLines: {
              display: false
            }
          }]
        },
        legend: {
          display: false
        }
      })
    }
  }
}

function prepareDatasets(djangoDataset, playersCount) {
  const datasets = [];
  for (let i = 0; i < playersCount; i++) {
    let values = djangoDataset.data.map(function (el) { return el[i] });
    let dataset = {
      label: djangoDataset.columns[i],
      borderColor: Vue.prototype.$colors[i],
      backgroundColor: Vue.prototype.$colors[i] + '33',
      borderWidth: 5,
      pointBackgroundColor: Vue.prototype.$colors[i],
      pointRadius: function(context) {
        var index = context.dataIndex;
        return index === values.length-1 ? 12 : 0;
      },
      data: values,
    };
    datasets.push(dataset);
  }
  return datasets;
}
</script>

<style>
.chart {
  height: 75vh;
}
</style>
