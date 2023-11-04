<template>
  <div>
    <b-card title="Sample Information" tag="article" class="mb-2">
      <b-table responsive id="sampleTable" :items="sampleData" :per-page="samplePerPage"
        :current-page="sampleCurrentPage" head-variant="light"
        :fields="fieldsSample" :sort-by.sync="sortBy" :sort-desc.sync="sortDesc" sort-icon-left>
      </b-table>
      <b-pagination v-model="sampleCurrentPage" :total-rows="sampleTableRows" :per-page="samplePerPage"
        align="right" aria-controls="sampleTable">
      </b-pagination>
    </b-card>
    <b-card title="Predicted Age (Double-click on the table to see a bar chart of predicted ages)" tag="article" class="mb-2">
      <b-table responsive id="ageTable" :items="ageData" :per-page="agePerPage"
        :current-page="ageCurrentPage" head-variant="light"  @row-dblclicked="drawBar"
        :fields="fields" :sort-by.sync="sortBy" :sort-desc.sync="sortDesc" sort-icon-left>
      </b-table>
      <b-pagination v-model="ageCurrentPage" :total-rows="ageTableRows" :per-page="agePerPage"
        align="right" aria-controls="ageTable">
      </b-pagination>
    </b-card>
    <b-card title="Predicted Age" tag="article" class="mb-2" v-show="showBar">
      <v-chart autoresize :option="predAgeOption" style="height: 300px"></v-chart>
    </b-card>
    <!-- <b-card title="Predicted Age Metric" tag="article" class="mb-2">
      <b-table responsive :items="errorData" head-variant="light"></b-table>
    </b-card> -->
  </div>
</template>

<script>
export default {
  data () {
    return {
      agePerPage: 5,
      ageCurrentPage: 1,
      samplePerPage: 5,
      sampleCurrentPage: 1,
      sampleData: [],
      errorData: [],
      // sampleData: [{
      //   'sampleID': 'GSM1051525',
      //   'Age': 78,
      //   'Age_unit': 'Year',
      //   'Gender': 'f',
      //   'Race': 'Yellow',
      //   'Tissue': 'PBL',
      //   'Country': 'United Kingdom',
      //   'Disease': 'rheumatoid arthritis',
      //   'Condition': '',
      //   'Platform': '450K',
      //   'Supplementary_Instructions': 'smoking status: current'
      // },
      // {
      //   'sampleID': 'GSM1051526',
      //   'Age': 67,
      //   'Age_unit': 'Year',
      //   'Gender': 'f',
      //   'Race': 'Yellow',
      //   'Tissue': 'PBL',
      //   'Country': 'United Kingdom',
      //   'Disease': 'rheumatoid arthritis',
      //   'Condition': '',
      //   'Platform': '450K',
      //   'Supplementary_Instructions': 'smoking status: current'
      // },
      // {
      //   'sampleID': 'GSM1051527',
      //   'Age': 53,
      //   'Age_unit': 'Year',
      //   'Gender': 'f',
      //   'Race': 'Yellow',
      //   'Tissue': 'PBL',
      //   'Country': 'United Kingdom',
      //   'Disease': 'rheumatoid arthritis',
      //   'Condition': '',
      //   'Platform': '450K',
      //   'Supplementary_Instructions': 'smoking status: current'
      // },
      // {
      //   'sampleID': 'GSM1051528',
      //   'Age': 23,
      //   'Age_unit': 'Year',
      //   'Gender': 'f',
      //   'Race': 'Yellow',
      //   'Tissue': 'PBL',
      //   'Country': 'United Kingdom',
      //   'Disease': 'rheumatoid arthritis',
      //   'Condition': '',
      //   'Platform': '450K',
      //   'Supplementary_Instructions': 'smoking status: current'
      // },
      // {
      //   'sampleID': 'GSM1051529',
      //   'Age': 12,
      //   'Age_unit': 'Year',
      //   'Gender': 'f',
      //   'Race': 'Yellow',
      //   'Tissue': 'PBL',
      //   'Country': 'United Kingdom',
      //   'Disease': 'rheumatoid arthritis',
      //   'Condition': '',
      //   'Platform': '450K',
      //   'Supplementary_Instructions': 'smoking status: current'
      // },
      // {
      //   'sampleID': 'GSM1051556',
      //   'Age': 49,
      //   'Age_unit': 'Year',
      //   'Gender': 'm',
      //   'Race': 'Yellow',
      //   'Tissue': 'PBL',
      //   'Country': 'United Kingdom',
      //   'Disease': 'rheumatoid arthritis',
      //   'Condition': '',
      //   'Platform': '450K',
      //   'Supplementary_Instructions': 'smoking status: current'
      // }],
      ageData: [],
      showBar: false,
      sortBy: 'sampleID',
      sortDesc: false,
      fields: [
        { key: 'sampleID', sortable: true },
        { key: 'Age', sortable: true, class: 'text-center' },
        { key: 'HorvathAge', sortable: false },
        { key: 'Skin&BloodClock', sortable: false },
        { key: 'ZhangBlupredAge', sortable: false },
        { key: 'HannumAge', sortable: false },
        { key: 'WeidnerAge', sortable: false },
        { key: 'LinAge', sortable: false },
        { key: 'PedBE', sortable: false },
        { key: 'FeSTwo', sortable: false },
        { key: 'MEAT', sortable: false },
        { key: 'AltumAge', sortable: false },
        { key: 'PhenoAge', sortable: false },
        { key: 'BNN', sortable: false },
        { key: 'EPM', sortable: false },
        { key: 'CorticalClock', sortable: false },
        { key: 'VidalBraloAge', sortable: false }
      ],
      fieldsSample: [
        { key: 'sampleID', sortable: true },
        { key: 'Age', sortable: true, class: 'text-center' },
        { key: 'Age_unit', sortable: false },
        { key: 'Gender', sortable: false },
        { key: 'Race', sortable: false },
        { key: 'Tissue', sortable: false },
        { key: 'Disease', sortable: false },
        { key: 'Condition', sortable: false },
        { key: 'Platform', sortable: false }
      ],
      predAgeOption: {}
    }
  },
  computed: {
    sampleTableRows () {
      return this.sampleData.length
    },
    ageTableRows () {
      return this.ageData.length
    },
    errorTableRows () {
      return this.errorData.length
    }
  },
  methods: {
    drawBar (item) {
      let xlable = Object.keys(item)
      let data = Object.values(item)
      xlable.splice(0, 2)
      data.splice(0, 2)
      this.predAgeOption = {
        title: {
          text: item['sampleID'],
          left: 'center'
        },
        xAxis: {
          type: 'category',
          axisLabel: {
            rotate: 45
          },
          data: xlable
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: data,
            type: 'bar'
          }
        ]
      }
      this.showBar = true
    }
  },
  mounted () {
    // this.sampleData = JSON.parse(sessionStorage['data'])
    this.sampleData = JSON.parse(sessionStorage['sampleData'])
    this.ageData = JSON.parse(sessionStorage['predAgeData'])
  }
}

</script>
<style scoped>
</style>
