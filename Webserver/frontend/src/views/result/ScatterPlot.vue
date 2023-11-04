<template>
    <div style="width:100vw; max-width: 100%;">
      <b-row>
        <b-card-group class="col-md-4" v-for="(clock, index) in clocks" :key="index">
          <b-card :header=clock tag="article" class="mb-2">
            <v-chart autoresize :option="chartData[index]" style="height: 380px"></v-chart>
          </b-card>
          </b-card-group>
        </b-row>
    </div>
  </template>

<script>
import * as ecStat from 'echarts-stat'
import * as echarts from 'echarts'
export default {
  data () {
    return {
      clocks: [],
      chartData: [],
      matric: [3.51, 4.58, 0.98]
    }
  },
  methods: {
    draw () {
      echarts.registerTransform(ecStat.transform.regression)
      const predAge = JSON.parse(sessionStorage['predAgeData'])
      for (let clock of this.clocks) {
        let axisData = []
        for (let i = 0; i < predAge.length; i++) {
          const age = predAge[i].Age
          const predage = predAge[i][clock]
          const newArr = [age, predage]
          axisData.push(newArr)
        }
        const option = {
          dataset: [
            {
              source: axisData
            },
            {
              transform: {
                type: 'ecStat:regression'
                // 'linear' by default.
                // config: { method: 'linear', formulaOn: 'end'}
              }
            }
          ],
          // title: {
          //   text: 'MAE=' + this.matric[0] + '  RMSE=' + this.matric[1] + '  R=' + this.matric[2],
          //   left: 'center',
          //   top: 10
          // },
          tooltip: {
            // trigger: 'axis',
            axisPointer: {
              type: 'cross'
            }
          },
          xAxis: {
            name: 'Year',
            splitLine: {
              lineStyle: {
                type: 'dashed'
              }
            }
          },
          yAxis: {
            name: 'Year',
            splitLine: {
              lineStyle: {
                type: 'dashed'
              }
            }
          },
          series: [
            {
              symbolSize: 5,
              // data: axisData,
              type: 'scatter',
              datasetIndex: 0
            },
            {
              name: 'line',
              type: 'line',
              datasetIndex: 1,
              symbolSize: 0.1,
              symbol: 'circle',
              label: { show: true, fontSize: 16 },
              labelLayout: { dx: -20 },
              encode: { label: 2, tooltip: 1 }
            }
          ]
        }
        this.chartData.push(option)
      }
    }
  },
  mounted () {
    this.clocks = sessionStorage['clocksName'].split(',')
    this.draw()
  }
}

</script>
  <style scoped>
  </style>
