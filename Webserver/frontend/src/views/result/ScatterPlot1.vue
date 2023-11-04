<template>
  <div>
    <b-row>
      <b-card-group class="col-md-4" v-for="(clock, index) in clocks" :key="index">
        <b-card :header=clock tag="article" class="mb-2">
          <v-chart autoresize :option="optionAge" style="height: 300px"></v-chart>
        </b-card>
        </b-card-group>
      </b-row>
  </div>
</template>

<script>
export default {
  data () {
    return {
      clocks: [],
      data: [
        [37, 34.55],
        [47, 60.28],
        [35, 55.52],
        [16, 47.52],
        [37, 46.89],
        [38, 36.55],
        [20, 40.65],
        [28, 33.38],
        [33, 45.23],
        [25, 50.55],
        [48, 41.6],
        [44, 50.55],
        [68, 67.86],
        [35, 41.32],
        [52, 61.96],
        [42, 53.66],
        [27, 43.88],
        [52, 53.22],
        [44, 43.47],
        [27, 52.62],
        [29, 30.56],
        [28, 41.55],
        [20, 29.16],
        [30, 61.3],
        [18, 60.03],
        [69, 79.9],
        [37, 46.95],
        [47, 56.21],
        [35, 88.16],
        [16, 56.08],
        [24, 49.99],
        [37, 62.74],
        [38, 55.77],
        [20, 50.24],
        [28, 45.24],
        [33, 62.37],
        [25, 56.56],
        [48, 73.05],
        [44, 52.49],
        [68, 70.92],
        [27, 53.16],
        [52, 51.23],
        [44, 58.59],
        [27, 63.08],
        [29, 44.51],
        [28, 58.05],
        [20, 41.05],
        [30, 59.87],
        [18, 73.26],
        [69, 71.73]
      ],
      optionAge: {
        xAxis: {},
        yAxis: {},
        series: [
          {
            symbolSize: 20,
            data: [
              [10.0, 8.04],
              [8.07, 6.95],
              [13.0, 7.58],
              [9.05, 8.81],
              [11.0, 8.33],
              [14.0, 7.66],
              [13.4, 6.81],
              [10.0, 6.33],
              [14.0, 8.96],
              [12.5, 6.82],
              [9.15, 7.2],
              [11.5, 7.2],
              [3.03, 4.23],
              [12.2, 7.83],
              [2.02, 4.47],
              [1.05, 3.33],
              [4.05, 4.96],
              [6.03, 7.24],
              [12.0, 6.26],
              [12.0, 8.84],
              [7.08, 5.82],
              [5.02, 5.68]
            ],
            type: 'scatter'
          }
        ]
      },
      target: [3.3, 0.9858, 0.0006]
    }
  },
  methods: {
    setPoint () {
      let myCharts = document.getElementsByClassName('myChart')
      for (let i = 0; i < myCharts.length; i++) {
        let myChart = this.$echarts.init(myCharts[i])
        myChart.setOption(
          {
            tooltip: {
              trigger: 'axis',
              axisPointer: {
                type: 'cross'
              }
            },
            title: {
              subtext: 'error:' + this.target[0] + ' r=' + this.target[1] + ' p=' + this.target[2]
            },
            xAxis: [{
              // gridIndex: 0,
              name: 'Age(y)',
              nameGap: 25,
              nameLocation: 'center'
            }],
            yAxis: [{
              // gridIndex: 0,
              name: 'PredAge(y)',
              nameGap: 25,
              nameLocation: 'center'
            }],
            series: [{
              name: 'male',
              type: 'scatter',
              data: this.data
            }]
          },
          true
        )
      }
    }
  },
  created () {
    this.clocks = sessionStorage['clocksName'].split(',')
  },
  mounted () {
    console.log()
    this.setPoint()
  }
}

</script>
<style scoped>
.myChart{
  width: 360px;
  height: 300px;
}
</style>
