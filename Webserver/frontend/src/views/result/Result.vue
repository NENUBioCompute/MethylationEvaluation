<template>
  <div style="width: 95%; margin: auto; margin-top: 50px;">
    <b-tabs
    active-nav-item-class="font-weight-bold text-uppercase text-danger"
    active-tab-class="font-weight-bold text-success"
    content-class="mt-3">
    <b-tab title="Predicted Result Table" active>
        <Table/>
    </b-tab>
    <b-tab title="Predicted Result Plot">
      <Plot/>
    </b-tab>
    <b-tab title="Predicted Result Scatter Plot">
      <ScatterPlot/>
    </b-tab>
  </b-tabs>
  </div>
</template>

<script>
import Table from './Table.vue'
import Plot from './Plot.vue'
import ScatterPlot from './ScatterPlot.vue'

export default {
  data () {
    return {
      gender: ['male', 'male', 'female'],
      selectGender: ['male', 'male', 'female'],
      clocks: [],
      datasetIDs: []
    }
  },

  components: { Table, Plot, ScatterPlot },

  methods: {
    processData () {
      if (this.$store.state.clockList.length !== 0) {
        sessionStorage.setItem('clocksName', this.$store.state.clockList)
        sessionStorage.setItem('model', this.$store.state.model)
        sessionStorage.setItem('data', JSON.stringify(this.$store.state.datasts))
        const data = []
        const predAge = []
        let genderNum = {}
        let ageNum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        const datasets = JSON.parse(sessionStorage['data'])
        let diseaseNum = {}
        let tissueNum = {}
        let raceNum = {}
        for (const dataset of datasets) {
          for (let index = 0; index < dataset['ID'].length; index++) {
            // 年龄数据
            const age = dataset['TrueAge'][index]
            switch (true) {
              case age < 0:
                ageNum[0] += 1
                break
              case age >= 0 && age < 10:
                ageNum[1] += 1
                break
              case age >= 10 && age < 20:
                ageNum[2] += 1
                break
              case age >= 20 && age < 30:
                ageNum[3] += 1
                break
              case age >= 30 && age < 40:
                ageNum[4] += 1
                break
              case age >= 40 && age < 50:
                ageNum[5] += 1
                break
              case age >= 50 && age < 60:
                ageNum[6] += 1
                break
              case age >= 60 && age < 70:
                ageNum[7] += 1
                break
              case age >= 70 && age < 80:
                ageNum[8] += 1
                break
              case age >= 80 && age < 90:
                ageNum[9] += 1
                break
              case age >= 90 && age < 100:
                ageNum[10] += 1
                break
              case age >= 100:
                ageNum[11] += 1
                break
            }
            // 性别数据
            if (dataset['Gender'] && genderNum[dataset['Gender'][index]]) {
              genderNum[dataset['Gender'][index]] += 1
            } else {
              genderNum[dataset['Gender'][index]] = 1
            }
            // 疾病数据
            if (dataset['Disease'] && diseaseNum[dataset['Disease'][index]]) {
              diseaseNum[dataset['Disease'][index]] += 1
            } else {
              diseaseNum[dataset['Disease'][index]] = 1
            }
            // 组织数据
            if (dataset['Tissue'] && tissueNum[dataset['Tissue'][index]]) {
              tissueNum[dataset['Tissue'][index]] += 1
            } else {
              tissueNum[dataset['Tissue'][index]] = 1
            }
            // 人种数据
            if (dataset['Race'] && raceNum[dataset['Race'][index]]) {
              raceNum[dataset['Race'][index]] += 1
            } else {
              raceNum[dataset['Race'][index]] = 1
            }
            // 样本数据
            const sample = {
              'sampleID': dataset['ID'][index],
              'Age': dataset['TrueAge'][index],
              'Age_unit': dataset['Age_unit'],
              'Gender': dataset['Gender'][index],
              'Race': dataset['Race'][index],
              'Tissue': dataset['Tissue'][index],
              'Disease': dataset['Disease'][index],
              'Condition': dataset['Condition'][index],
              'Platform': dataset['Platform']
            }
            // 预测年龄
            const pred = {
              'dataset': dataset['Dataset'],
              'sampleID': dataset['ID'][index],
              'Age': dataset['TrueAge'][index]
              // 'HorvathAge': dataset['PredAge']['HorvathAge'][index],
              // 'Skin&BloodClock': dataset['PredAge']['Skin&BloodClock'][index],
              // 'ZhangBlupredAge': dataset['PredAge']['ZhangBlupredAge'][index],
              // 'HannumAge': dataset['PredAge']['HannumAge'][index],
              // 'WeidnerAge': dataset['PredAge']['WeidnerAge'][index]
              // 'LinAge': dataset['PredAge']['LinAge'][index],
              // 'PedBE': dataset['PredAge']['PedBE'][index],
              // 'FeSTwo': dataset['PredAge']['FeSTwo'][index],
              // 'MEAT': dataset['PredAge']['MEAT'][index],
              // 'AltumAge': dataset['PredAge']['AltumAge'][index],
              // 'PhenoAge': dataset['PredAge']['PhenoAge'][index],
              // 'BNN': dataset['PredAge']['BNN'][index],
              // 'EPM': dataset['PredAge']['EPM'][index],
              // 'CorticalClock': dataset['PredAge']['CorticalClock'][index],
              // 'VidalBraloAge': dataset['PredAge']['VidalBraloAge'][index]
              // 'PerSEClock': dataset['PredAge']['PerSEClock'][index]
            }
            if (dataset['PredAge']) {
              const predAgeKeys = Object.keys(dataset['PredAge'])
              for (const key of predAgeKeys) {
                pred[key] = dataset['PredAge'][key][index]
              }
            }
            data.push(sample)
            predAge.push(pred)
          }
        }
        console.log(datasets)
        sessionStorage.setItem('sampleData', JSON.stringify(data))
        sessionStorage.setItem('predAgeData', JSON.stringify(predAge))
        sessionStorage.setItem('genderNum', JSON.stringify(genderNum))
        sessionStorage.setItem('ageNum', JSON.stringify(ageNum))
        sessionStorage.setItem('diseaseNum', JSON.stringify(diseaseNum))
        sessionStorage.setItem('tissueNum', JSON.stringify(tissueNum))
        sessionStorage.setItem('raceNum', JSON.stringify(raceNum))
      }
    },
    allGender () {
      this.selectGender = this.gender
    },
    Male () {
      const select = []
      for (const item of this.gender) {
        if (item === 'male') {
          select.push(item)
        }
      }
      this.selectGender = select
    },
    Female () {
      const select = []
      for (const item of this.gender) {
        if (item === 'female') {
          select.push(item)
        }
      }
      this.selectGender = select
    }
  },
  created () {
    this.processData()
  }
}

</script>
<style scoped>
</style>
