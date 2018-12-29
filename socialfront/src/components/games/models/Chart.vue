<script>
/* eslint-disable */
import { Line } from 'vue-chartjs'
import moment from 'moment'

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
    const data = this.chartdata;
    const playersCount = data.columns.length;
    const datasets = prepareDatasets(data, playersCount, this.gradient);
    const labels = data.index.map(function(e) {
      return moment(new Date(e).toString()).format("MM/DD/YYYY")
    });
    const x = {
      labels: labels,
      datasets: datasets
    }
    this.renderChart(x, this.options)
  }
}
const colors = ['#007bff', '#6f42c1', '#fd7e14', '#28a745', '#17a2b8'];

function prepareDatasets(djangoDataset, playersCount, gradient) {
  const datasets = [];
  for(let i = 0; i < playersCount; i++) {
    let values = djangoDataset.data.map(function(el) { return el[i] });
    let dataset = {
      label: djangoDataset.columns[i],
      borderColor: colors[i],
      borderWidth: 3,
      pointRadius: 0,
      data: values
    };
    datasets.push(dataset);
  }
  return datasets;
}
</script>

<style>
</style>
