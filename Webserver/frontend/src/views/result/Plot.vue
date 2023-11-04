<template>
  <div style="width:100vw; max-width: 100%;">
    <b-row>
      <b-col cols="3">
        <b-card header="Age Ratio Plot" tag="article" class="mb-2">
          <v-chart autoresize :option="optionAge" style="height: 300px"></v-chart>
        </b-card>
      </b-col>
      <b-col cols="3">
        <b-card header="Gender Ratio Plot" tag="article" class="mb-2">
          <v-chart autoresize :option="optionGender" style="height: 300px"></v-chart>
        </b-card>
      </b-col>
      <b-col v-show=showDisease cols="6">
        <b-card header="Disease Ratio Plot" tag="article" class="mb-2">
          <v-chart autoresize :option="optionDisease" style="height: 300px"></v-chart>
        </b-card>
      </b-col>
      <b-col v-show=showTissue cols="6">
        <b-card header="Tissue Ratio Plot" tag="article" class="mb-2">
          <v-chart autoresize :option="optionTissue" style="height: 300px"></v-chart>
        </b-card>
      </b-col>
      <b-col v-show=showRace cols="6">
        <b-card header="Race Ratio Plot" tag="article" class="mb-2">
          <v-chart autoresize :option="optionRace" style="height: 300px"></v-chart>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {
  data () {
    return {
      optionAge: {},
      optionGender: {
        title: {
          text: 'Diease Ratio',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            type: 'pie',
            radius: '50%',
            data: [
              { value: 58, name: 'Male' },
              { value: 49, name: 'Female' },
              { value: 49, name: 'Unknown' }
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      },
      optionDisease: {},
      optionTissue: {
        title: {
          text: 'Diease Ratio',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            type: 'pie',
            radius: '50%',
            data: [
              { value: 25, name: 'T cell' },
              { value: 12, name: 'PBMC' },
              { value: 15, name: 'Colon' },
              { value: 33, name: 'Whole blood' }
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      },
      optionRace: {
        title: {
          text: 'Diease Ratio',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            type: 'pie',
            radius: '50%',
            data: [
              { value: 13, name: 'Black' },
              { value: 27, name: 'Japan' },
              { value: 20, name: 'Unknown' }
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      },
      showDisease: false,
      showTissue: false,
      showRace: false
    }
  },
  methods: {
    drawChart () {
      const genderNum = JSON.parse(sessionStorage['genderNum'])
      const ageNum = JSON.parse(sessionStorage['ageNum'])
      const diseaseNum = JSON.parse(sessionStorage['diseaseNum'])
      const tissueNum = JSON.parse(sessionStorage['tissueNum'])
      const raceNum = JSON.parse(sessionStorage['raceNum'])
      let genderData = []
      let diseaseData = []
      let tissueData = []
      let raceData = []
      for (const item in genderNum) {
        const num = {
          value: genderNum[item], name: item
        }
        genderData.push(num)
      }
      console.log(genderData)
      for (const item in diseaseNum) {
        const num = {
          value: diseaseNum[item], name: item
        }
        diseaseData.push(num)
      }
      for (const item in tissueNum) {
        const num = {
          value: tissueNum[item], name: item
        }
        tissueData.push(num)
      }
      for (const item in raceNum) {
        const num = {
          value: raceNum[item], name: item
        }
        raceData.push(num)
      }
      this.optionGender = {
        title: {
          // text: 'Gender Ratio',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'right',
          right: 20,
          top: 0,
          bottom: 20
        },
        series: [
          {
            type: 'pie',
            radius: '50%',
            data: genderData,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      this.optionAge = {
        title: {
          // text: 'Age Ratio',
          left: 'center'
        },
        xAxis: {
          type: 'category',
          data: ['< 0', '0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100', '> 100'],
          axisLabel: {
            interval: 0,
            rotate: 40
          }
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: ageNum,
            type: 'bar'
          }
        ]
      }
      this.optionDisease = {
        title: {
          // text: 'Diease Ratio',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'right',
          right: 20,
          top: 0,
          bottom: 20,

          type: 'scroll' // 数据过多时，分页显示
        },
        series: [
          {
            type: 'pie',
            radius: '50%',
            data: diseaseData,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      this.optionTissue = {
        title: {
          // text: 'Diease Ratio',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'right',
          right: 20,
          top: 0,
          bottom: 20,

          type: 'scroll' // 数据过多时，分页显示
        },
        series: [
          {
            type: 'pie',
            radius: '50%',
            data: tissueData,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      this.optionRace = {
        title: {
          // text: 'Diease Ratio',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'right',
          right: 20,
          top: 0,
          bottom: 20,

          type: 'scroll' // 数据过多时，分页显示
        },
        series: [
          {
            type: 'pie',
            radius: '50%',
            data: raceData,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
    },
    changeModel () {
      if (sessionStorage['model'] === 'datasets') {
        this.showDisease = true
        this.showTissue = true
        this.showRace = true
      }
      // if (sessionStorage['model'] === 'disease') {
      //   this.showTissue = false
      //   this.showRace = false
      //   this.showDisease = false
      // } else if (sessionStorage['model'] === 'tissue') {
      //   this.showTissue = false
      //   this.showDisease = false
      //   this.showRace = false
      // } else if (sessionStorage['model'] === 'race') {
      //   this.showRace = false
      //   this.showTissue = false
      //   this.showDisease = false
      // }
    }
  },
  mounted () {
    this.drawChart()
    this.changeModel()
  }
}
</script>
