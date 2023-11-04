<template>
  <div class="clocksBox">
    <b-row><h4>Currently Available Clocks in <i style="color: red;">DNAm Clocks</i> are Listed in Table Below and you can choose them</h4></b-row><hr/>
    <b-row>
      <div style="float: left;">
      <b-button variant="outline-primary" size="sm" @click="selectAllRows">Select all</b-button>
      <b-button variant="outline-danger" style="margin-left: 5px;" size="sm" @click="clearSelected">Clear selected</b-button>
    </div>
    </b-row>
    <b-row>
      <b-table id="clocksTable" :fields="fields" :items="clocksData" 
      head-variant="light" :per-page="clocksPerPage"
      ref="selectableTable"
      selectable
      :select-mode="selectMode"
      :current-page="clocksCurrentPage" :pagination="true"  @row-selected="onRowSelected" responsive>
      <template v-slot:cell(Reference)="data"><!--cell()用来收集单元格的数据对象-->
          <span v-html="data.value"></span>
      </template>
      <template v-slot:cell(ClockName)="data">
        <b-link :to="getLink(data.item.id)" target="_blank" style="color: ;">{{ data.value }}</b-link>
      </template>
       <template v-slot:cell(selected)="{ rowSelected }">
       <template v-if="rowSelected">
          <span style="margin-left: 25px;" aria-hidden="true">&check;</span>
        </template>
      </template>
    </b-table>
    <!--<b-pagination v-model="clocksCurrentPage" :total-rows="clocksTableRows" :per-page="clocksPerPage"
        align="right" aria-controls="sampleTable">
      </b-pagination>-->
      <b-row>
     <b-button variant="danger" v-b-modal.modal1 size="lg" style="margin-left: 10%;">Upload</b-button></b-row>
     <b-modal id="modal1" ref="my-modal" scrollable hide-footer title="Tip">
      <div class="d-block text-center">
        <h4>The methods you chosen are:</h4>
     <ul>
      <li v-for="clocksData in selected" :key="clocksData">{{ clocksData.ClockName }}<hr></li>
    </ul>
      </div>
      <span>
      <b-button class="mt-2" variant="outline-danger" style="width: 100%;" @click="goToPage()">upload</b-button>
      <b-button class="mt-2" variant="outline-warning" block @click="toggleModal">check again</b-button></span>
    </b-modal>
    </b-row>
  </div>
</template>
<script>
export default {
  data () {
    return {
      selected: [],
      clocksPerPage: 100,
      clocksCurrentPage: 1,
      fields: ['Selected','ClockName', 'FeaturesNum', 'LifePhase', 'Platform', 'Tissue', 'Reference'],
      clocksData: [
        {
          id:1,
          'ClockName': 'Horvath Clock',
          'Tissue': 'Pan-tissue',
          'FeaturesNum': 353,
          'Platform': 'HM450',
          'Error(Years)': 3.5,
          'Reference': "<a href='https://doi.org/10.1186/gb-2013-14-10-r115'>Horvath, 2013</a>",
          'LifePhase': 'lifespan'
        },
        {
          id:2,
          'ClockName': 'OriginalMethod',
          'Tissue': 'Pan-tissue',
          'FeaturesNum': 24516,
          'Platform': '27K,450K,850K',
          'Reference': "<a href='#'>PerSEClock</a>",
          'Error(Years)': 3.0,
          'LifePhase': 'lifespan'
        },
        {
          'ClockName': 'Skin&Blood Clock',
          'Tissue': 'Blood,Epithelium,Saliva,Skin',
          'FeaturesNum': '391',
          'Platform': 'HM450, HMEPIC',
          'Reference': "<a href='https://doi.org/10.18632/aging.101508'>Horvath et al., 2018</a>",
          'Error(Years)': 4.5,
          'LifePhase': 'lifespan'
        },
        {
          'ClockName': 'Zhang Clock',
          'Tissue': 'Adipose,Blood,Brain,Breast,Liver,Saliva,Uterine',
          'FeaturesNum': 514,
          'Platform': 'HM450, HMEPIC',
          'Reference': "<a href='https://doi.org/10.1186/s13073-019-0667-1'>Zhang et al., 2019</a>",
          'Error(Years)': 5.6,
          'LifePhase': 'lifespan'
        },
        {
          'ClockName': 'Hannum Clock',
          'Tissue': 'Blood',
          'FeaturesNum': '71',
          'Platform': 'HM450',
          'Reference': "<a href='https://doi.org/10.1016/j.molcel.2012.10.016'>Hannum et al., 2013</a>",
          'Error(Years)': 3.8,
          'LifePhase': 'lifespan'
        },
        {
          'ClockName': 'Weidner Clock',
          'Tissue': 'Blood',
          'FeaturesNum': '3',
          'Platform': 'HM27',
          'Reference': "<a href='https://doi.org/10.18632/aging.101414'>Weidner et al., 2014</a>",
          'Error(Years)': 5.6,
          'LifePhase': 'lifespan'
        },
        {
          'ClockName': 'Lin Clock',
          'Tissue': 'Blood',
          'FeaturesNum': 102,
          'Platform': 'HM450',
          'Reference': "<a href='https://doi.org/10.18632/aging.100908'>Lin et al., 2016</a>",
          'Error(Years)': 0.35,
          'LifePhase': 'lifespan'
        },
        {
          'ClockName': 'PedBE',
          'Tissue': 'Buccal,Epithelial',
          'FeaturesNum': '94',
          'Platform': 'HM450',
          'Reference': "<a href='https://doi.org/10.1073/pnas.1820843116'>McEwen et al., 2020</a>",
          'Error(Years)': 5.6,
          'LifePhase': 'adult'
        },
        {
          'ClockName': 'FeSTwo',
          'Tissue': 'Multi',
          'FeaturesNum': 70,
          'Platform': 'HM450',
          'Reference': "<a href='https://doi.org/10.1016/j.compbiomed.2020.104008'>Wei et al., 2020</a>",
          'Error(Years)': 5.6,
          'LifePhase': 'adult'
        },
        {
          'ClockName': 'MEAT',
          'Tissue': 'skeletal muscle',
          'FeaturesNum': 156,
          'Platform': 'HM27, HM450, HMEPIC',
          'Reference': "<a href='https://doi.org/10.1002/jcsm.12556'>Voisin et al., 2020</a>",
          'Error(Years)': 5.6,
          'LifePhase': 'adult'
        },
        {
          'ClockName': 'AltumAge',
          'Tissue': 'Multi',
          'FeaturesNum': 20318,
          'Platform': 'HM27, HM450, HMEPIC',
          'Reference': "<a href='https://www.nature.com/articles/s41514-022-00085-y'>Camillo et al., 2022</a>",
          'Error(Years)': 5.6,
          'LifePhase': 'adult'
        },
        {
          'ClockName': 'PhenoAge',
          'Tissue': 'Multi',
          'FeaturesNum': 513,
          'Platform': 'HM27, HM450, HMEPIC',
          'Reference': "<a href='https://doi.org/10.18632/aging.101414'>Levine  et al., 2018</a>",
          'Error(Years)': 5.6,
          'LifePhase': 'adult'
        },
        {
          'ClockName': 'BNN',
          'Tissue': 'Multi',
          'FeaturesNum': 353,
          'Platform': 'HM27, HM450',
          'Reference': "<a href='https://doi.org/10.1101/2020.04.21.052605'>Gonzalez et al., 2020</a>",
          'Error(Years)': 5.6,
          'LifePhase': 'adult'
        },
        {
          'ClockName': 'EPM',
          'Tissue': 'Multi',
          'FeaturesNum': 1000,
          'Platform': 'HM450',
          'Reference': "<a href='https://doi.org/10.1093/bioinformatics/btaa585'>Farrell et al., 2020</a>",
          'Error(Years)': 5.6,
          'LifePhase': 'lifespan'
        },
        {
          'ClockName': 'Cortical Clock',
          'Tissue': 'Cortex',
          'FeaturesNum': 347,
          'Platform': 'HM450',
          'Reference': "<a href='https://doi.org/10.1093/brain/awaa334'>Shireby et al., 2020</a>",
          'Error(Years)': 5.6,
          'LifePhase': 'lifespan'
        },
        {
          'ClockName': 'VidalBralo Clock',
          'Tissue': 'Blood',
          'FeaturesNum': 8,
          'Platform': 'HM27, HM450',
          'Reference': "<a href='https://doi.org/10.3389/fgene.2016.00126'> Vidal-Bralo et al., 2016</a>",
          'Error(Years)': 5.6,
          'LifePhase': 'adult'
        }
      ]
    }
  },
  methods:{
      onRowSelected(items) {
        this.selected = items
      },
      selectAllRows() {
        this.$refs.selectableTable.selectAllRows()
      },
      clearSelected() {
        this.$refs.selectableTable.clearSelected()
      },
      showModal() {
      this.$refs.my-modal.show(); // 调用show()方法显示模态框
      },
      toggleModal() {
        this.$refs['my-modal'].toggle('#toggle-btn')// We pass the ID of the button that we want to return focus to
      },
      getLink(id) {
      // 根据不同的行元素id返回对应的页面路径
      if (id === 1) {
        return ;
      } else if(id===2){
          return '/original';
        }
   },
   goToPage() {
    this.$router.push({ path: '/Upload', query: { value: this.ClockNameFieldValue} });
    }
},
computed: {
    clocksTableRows () {
      return this.clocksData.length
    },
    ClockNameFieldValue() {
      return this.selected.map(item => item.ClockName);
    },
    /*selectedFieldValues() {
      if (this.selected) {
        return [this.selected.ClockName]; // 只将选中行的name字段值存储在数组中
      } else {
        return [];
      }
    }*/
  },
  created () {
    getClocks().then(res => {
      console.log(res.data)
      this.clocksData = res.data['data']
    })
  }
}

</script>
<style scoped>
  .clocksBox{
    margin: auto;
    margin-top: 20px;
    width: 90%;
  }
  ul{
    padding-left: 20px;
  }
</style>
