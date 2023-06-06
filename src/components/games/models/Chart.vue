<script>
/* eslint-disable */
import { Line } from 'vue-chartjs'
import moment from 'moment'

export default {
  extends: Line,
  props: {
    chartdata: { default: null },
    options: { default: null }
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
        animations: {
            tension: {
                duration: 200,
                easing: 'linear',
                from: 3,
                to: 0,
                loop: true
            }
        },
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          xAxes: [{
            type: 'time',
            time: {
              displayFormats: {
                quarter: 'MMM YYYY'
              }
            },
            ticks: {
              fontSize: 20,
              fontFamily: 'KoHo'
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
const colors = ['#fd7e14', '#007bff', '#6f42c1', '#28a745', '#17a2b8'];

function prepareDatasets(djangoDataset, playersCount) {
  const datasets = [];
  for (let i = 0; i < playersCount; i++) {
    let values = djangoDataset.data.map(function (el) { return el[i] });
    let dataset = {
      label: djangoDataset.columns[i],
      borderColor: colors[i],
      backgroundColor: colors[i] + '33',
      borderWidth: 1,
      pointRadius: 0,
      data: values,
      gridLines: {
        display: false
      },
    };
    datasets.push(dataset);
  }
  return datasets;
}
</script>

<style></style>
