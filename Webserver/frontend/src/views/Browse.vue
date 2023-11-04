<template>
  <div class="browse-box">
    <b-container fluid>
      <b-row class="my-1"><b-col><h3>Select Data</h3></b-col></b-row>
      <hr />
      <b-row class="my-1">
        <!--选择模式-->
        <b-col sm="2" md="auto">
          <b>Select Model:</b>
        </b-col>
        <b-col cols="4">
          <b-form-radio-group v-model="selectedModel" :options="optionsModel"  class="mb-3"
          value-field="item" text-field="name" @change="changeModel"></b-form-radio-group>
        </b-col>
        <!--跳转结果页-->
        <b-col>
          <b-button style="float: right" size="md" @click="result">Result</b-button>
        </b-col>
      </b-row>
      <!--未选择数据集时 提示-->
      <b-alert v-model="errorShow" variant="danger" show dismissible>Please Select Datasets and Clocks</b-alert>
      <b-row class="my-1">
        <!--模式列 数据集、组织、疾病或种族-->
        <b-col cols="9" style="border-right: 1px solid #e9ecef;">
          <b-row class="my-1">
            <!--表格全选或取消全选-->
            <b-col cols="6">
              <p>
                <b-button size="sm" @click="selectAllRows">Select all</b-button>
                <b-button size="sm" :disabled="selectedRows.length === 0" @click="clearSelected">Clear selected</b-button>
              </p>
            </b-col>
            <!--搜索-->
            <b-col cols="6">
            <b-form-group label="search" label-for="filter-input" label-cols-sm="3"
              label-align-sm="right" label-size="sm" class="mb-0">
            <b-input-group size="sm">
              <b-form-input
                id="filter-input" v-model="filter" type="search" placeholder="Type to Search">
              </b-form-input>
              <b-input-group-append>
                <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
              </b-input-group-append>
            </b-input-group>
            </b-form-group>
            </b-col>
          </b-row>
          <b-row class="my-1">
            <!--表格-->
            <b-overlay :show="loading" style="width: 100%" opacity=1>
            <b-table :per-page="perPage" responsive head-variant="light" :current-page="currentPage"
              :items="sampleData" :fields="fields" :filter="filter" ref="selectableTable"
              :sort-by.sync="sortBy" :sort-desc.sync="sortDesc" sort-icon-left
              @row-clicked="rowClicked" :tbody-tr-class="tbodyRowClass" primary-key="id" :busy="isBusy">
              <template v-slot:cell(selected)="{ item, field: { key } }" >
                <b-checkbox v-model="item[key]"></b-checkbox>
              </template>
              <!-- <template #table-busy>
                <div class="text-center text-danger my-2">
                  <b-spinner class="align-middle"></b-spinner>
                  <strong>Loading...</strong>
                </div>
              </template> -->
            </b-table>
          </b-overlay>
          </b-row>
          <b-row class="my-1">
            <b-col cols="4">
              <b-form-group
              label="Per page" label-for="per-page-select" label-size="sm" class="mb-0"
              label-cols-sm="6" label-cols-md="4" label-cols-lg="3" label-align-sm="right">
              <b-form-select
                id="per-page-select" v-model="perPage" :options="pageOptions" size="sm">
              </b-form-select>
            </b-form-group>
            </b-col>
            <b-col cols="8">
              <b-pagination
                v-model="currentPage" :total-rows="rows" :per-page="perPage"
                align="left" size="md" class="my-0">
              </b-pagination>
            </b-col>
          </b-row>
        </b-col>
        <b-col cols="3">
          <b>select Gender: </b>
          <b-form-checkbox-group
              v-model="selectedGender" :options="genderList" class="mb-3"
              value-field="item" text-field="name" disabled-field="notEnabled">
          </b-form-checkbox-group>
          <b>Select Clocks: </b>&nbsp;&nbsp;
          <b-badge to="/clocks" variant="danger">Clocks Info</b-badge>
          <b-form-group>
            <template v-slot:label>
              <b-form-checkbox style="color: blue"
                v-model="allSelectedClocks" :indeterminate="indeterminateClocks" aria-describedby="clocksList"
                aria-controls="clocksList" @change="toggleAllClocks" size="lg">
                {{ allSelectedClocks ? 'Un-select All' : 'Select All' }}
              </b-form-checkbox>
            </template>
            <b-container class="bv-example-row bv-example-row-flex-cols">
              <b-row>
                <b-form-group v-slot="{ ariaDescribedby }">
                  <b-form-checkbox-group
                    v-model="selectedClocks"
                    :options="clocksList"
                    :aria-describedby="ariaDescribedby"
                    name="flavour-2a"
                    stacked>
                  </b-form-checkbox-group>
                </b-form-group>
              </b-row>
            </b-container>
          </b-form-group>
        </b-col>
      </b-row>
      <!-- <b-row class="my-1">
        <b-button size="lg" @click="result">Result</b-button>
      </b-row> -->
    </b-container>
  </div>
</template>
<script>
import { getDatasets, getDisease, getRace, getTissue } from '../api'
export default {
  name: 'Browse',
  data () {
    return {
      fields: [
        { key: 'id', thClass: 'd-none', tdClass: 'd-none' },
        { key: 'selected', sortable: false },
        { key: 'Dataset', sortable: true },
        { key: 'AgeRange', sortable: false },
        { key: 'Age_unit', sortable: false },
        { key: 'SampleNum', sortable: true } ], // 表格列名 默认数据集列
      selectMode: 'multi', // 每次单击都会选择/取消选择该行
      filter: null,
      isBusy: false, // 表格loading
      currentPage: 1, // 表格当前页码 默认 1
      perPage: 5, // 表格每页显示的行数 默认 10
      // totalRows: 1, // 表格的总行数
      pageOptions: [10, 20, { value: 100, text: 'Show a lot' }], // 表格每页行数
      sortBy: 'Dataset', // 默认数据集名称排序
      sortDesc: false,
      optionsModel: [
        { item: 'datasets', name: 'Datasets' },
        { item: 'tissue', name: 'Tissue' },
        { item: 'disease', name: 'Disease' },
        { item: 'race', name: 'Race' }
      ], // 模式选择
      selectedModel: 'datasets', // 模式选择 默认数据集
      sampleData: [], // 表格数据
      datasetsData: [],
      diseaseData: [],
      tissueData: [],
      raceData: [],
      // sampleData: [],
      // sampleData: [],
      clocksList: ['HorvathAge', 'OriginalMethod','Skin&BloodClock', 'ZhangBlupredAge', 'HannumAge', 'WeidnerAge', 'LinAge',
        'PedBE', 'FeSTwo', 'MEAT', 'AltumAge', 'PhenoAge', 'BNN', 'EPM', 'CorticalClock', 'VidalBraloAge'], // 时钟列表
      genderList: ['Female', 'Male', 'Unknown'], // 性别列表
      selectedGender: ['Female', 'Male', 'Unknown'], // 默认性别全选
      selectedClocks: [],
      allSelectedClocks: false, // 是否全选时钟
      indeterminateClocks: false,
      clocksNum: 0, // 时钟个数
      errorShow: false, // 显示错误信息
      loading: false
    }
  },
  computed: {
    // 选中的行
    selectedRows () {
      return this.sampleData.filter(item => item.selected)
    },
    rows () {
      return this.sampleData.length
    }
  },
  methods: {
    tbodyRowClass (item) {
      /* Style the row as needed */
      if (item.selected) {
        return ['b-table-row-selected', 'table-primary', 'cursor-pointer']
      } else {
        return ['cursor-pointer']
      }
    },
    rowClicked (item) {
      if (item.selected) {
        this.$set(item, 'selected', false)
      } else {
        this.$set(item, 'selected', true)
      }
    },
    selectAllRows () {
      const left = (this.currentPage - 1) * this.perPage
      const right = this.currentPage * this.perPage - 1
      for (let i = left; i <= right; i++) {
        this.$set(this.sampleData[i], 'selected', true)
      }
    },
    clearSelected () {
      this.selectedRows.forEach((item) => {
        this.$delete(item, 'selected')
      })
    },
    toggleAllClocks (checked) {
      this.selectedClocks = checked ? this.clocksList.slice() : []
      this.clocksNum = this.selectedClocks.length
    },
    changeModel (value) {
      this.$store.commit('setModelState', value)
      if (value === 'datasets') {
        this.clearSelected()
        this.fields = [
          { key: 'selected', sortable: false },
          { key: 'Dataset', sortable: true },
          { key: 'AgeRange', sortable: false },
          { key: 'Age_unit', sortable: false },
          { key: 'SampleNum', sortable: true } ]
        this.sampleData = this.datasetsData
        return true
      }
      if (value === 'tissue') {
        this.clearSelected()
        this.fields = [
          { key: 'selected', sortable: false },
          { key: 'Tissues', sortable: true },
          { key: 'SampleNum', sortable: true } ]
        this.sampleData = this.tissueData
        return true
      }
      if (value === 'disease') {
        this.fields = [
          { key: 'selected', sortable: false },
          { key: 'Diseases', sortable: true },
          { key: 'SampleNum', sortable: true } ]
        this.sampleData = this.diseaseData
        return true
      }
      if (value === 'race') {
        this.clearSelected()
        this.fields = [
          { key: 'selected', sortable: false },
          { key: 'Races', sortable: true },
          { key: 'SampleNum', sortable: true } ]
        this.sampleData = this.raceData
        return true
      }
    },
    result () {
      const result = {}
      // result['geos'] = this.selectedGeoData
      result['clocks'] = this.selectedClocks
      this.$store.commit('setDatastsState', this.selectedRows)
      this.$store.commit('setClockListState', this.selectedClocks)
      // result['gender'] = this.selectedGender
      // result['disease'] = this.selectDisease
      // result['race'] = this.selectRace
      // result['country'] = this.selectCountry
      // console.log(result)
      if (this.selectedClocks.length !== 0) {
        this.$router.push({
          path: '/result'
        })
      } else {
        this.errorShow = true
      }
    }
  },

  watch: {
    selectedClocks (newVal, oldVal) {
      if (newVal.length === 0) {
        this.indeterminateClocks = false
        this.allSelectedClocks = false
      } else if (newVal.length === this.clocksList.length) {
        this.indeterminateClocks = false
        this.allSelectedClocks = true
      } else {
        this.indeterminateClocks = true
        this.allSelectedClocks = false
      }
    },
    selectedGeo (newVal, oldVal) {
      if (newVal.length === 0) {
        this.indeterminateGeo = false
        this.allSelectedGeo = false
      } else if (newVal.length === this.selectedGeoData.length) {
        this.indeterminateGeo = false
        this.allSelectedGeo = true
      } else {
        this.indeterminateGeo = true
        this.allSelectedGeo = false
      }
    }
  },
  created () {
    getDatasets().then(res => {
      this.sampleData = res.data['data']
      this.datasetsData = res.data['data']
    })
    getDisease().then(res => {
      this.diseaseData = res.data['data']
    })
    getTissue().then(res => {
      this.tissueData = res.data['data']
    })
    getRace().then(res => {
      this.raceData = res.data['data']
    })
  }
}
</script>
<style scoped>
.browse-box {
  width: 85%;
  margin: auto;
  margin-top: 20px;
}
</style>
