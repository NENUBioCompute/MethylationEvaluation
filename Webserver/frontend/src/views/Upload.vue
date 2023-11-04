<template>
  <div class="upload-box">
    <b-container fluid>
      <b-row class="my-1"><b-col><h2>Upload Your Data</h2></b-col></b-row><hr/>
      <b-alert v-model="errLogShow" variant="danger" show dismissible>Please login before uploading data</b-alert>
      <b-alert v-model="noFileShow" variant="danger" show dismissible>You must upload beta data and phenotype data</b-alert>
      <b-alert v-model="errFileNameShow" variant="danger" show dismissible>Your file name must match the requirements</b-alert>
      <b-alert v-model="errGeoIDShow" variant="danger" show dismissible>Beta Data and Phenotype Data must have the same GEO ID</b-alert>
      <b-alert v-model="errSamIDShow" variant="danger" show dismissible>Beta Data and Phenotype Data must have the same Sample ID</b-alert>
      <b-alert v-model="errHeadShow" variant="danger" show dismissible>Please Rank transfer your Beta Data and try again</b-alert>
      <b-alert v-model="errPhoneShow" variant="danger" show dismissible>ID Tissue disease condition Age Age_unit Gender Race Platform are required in phone</b-alert>
      <b-alert v-model="errIdShow" variant="danger" show dismissible>Id dismissed in phone flie</b-alert>
      <b-alert v-model="errAboveShow" variant="danger" show dismissible>More than 20 of datas are not allowed</b-alert>
      <b-row class="my-1">
        <b-col sm="8">
          <b-container>
            <b-row class="my-2">
              <b>DNA Methylation Beta Data (csv or zip)
              <i class="format" v-b-modal.modal-beta>(Beta Data Format)</i></b>
            </b-row>
            <b-row class="my-2">
              <b-form-file ref="beta-input" multiple v-model="betaFile" accept=".csv, .zip, .gz"></b-form-file>
              <b-progress v-show="dialogVisibleBeta" :value="betaProgress" max=100 class="mb-3"></b-progress>
              <b-modal id="modal-beta" title="Beta Data Format" ok-only>
                <img style="object-fit: contain; width: 95%;" src="../assets/beta.jpg" />
              </b-modal>
            </b-row>
            <b-row class="my-2">
              <b>Phenotype Data (csv or zip)<i class="format" v-b-modal.modal-pheno>(Phenotype Data Format)</i></b>
            </b-row>
            <b-row class="my-2">
              <b-form-file ref="pheno-input" multiple v-model="phenoFile" accept=".csv, .zip, .gz"></b-form-file>
              <b-progress v-show="dialogVisiblePheno" :value="betaProgress" max=100 class="mb-3"></b-progress>
              <b-modal id="modal-pheno" ok-only title="Phenotype Data Format">
                <img style="object-fit: contain; width: 95%;" src="../assets/pheno.png" />
              </b-modal>
            </b-row>
            <b-row class="my-2">
              <b>Select Tissues Of The Dataset</b>
            </b-row>
            <b-row class="my-2">
              <b-form-select
              class="mb-2 mr-sm-2 mb-sm-0"
              v-model="tissue"
              :options="options"
              id="inline-form-custom-select-pref">
              </b-form-select>
            </b-row>
            <b-row class="my-2">
              <b>Select Samples Age Unit</b>
            </b-row>
            <b-row class="my-2">
              <b-form-select
                class="mb-2 mr-sm-2 mb-sm-0"
                v-model="ageUnit"
                :options="ageUnitOptions"
                id="inline-form-custom-select-pref">
              </b-form-select>
            </b-row>
            <b-row>
              <b>Select NA Value Imputation Method</b>
            </b-row>
            <b-row class="my-2">
              <b-form-select
                class="mb-2 mr-sm-2 mb-sm-0"
                v-model="naImp"
                :options="naImpOptions"
                id="inline-form-custom-select-pref">
              </b-form-select>
            </b-row>
          </b-container>
        </b-col>
        <!--<b-col sm="4">
          <div style="border-left: 1px solid #e9ecef; padding-left: 12px; height: 100%;">
            <b>Select the Clocks</b>&nbsp;&nbsp;
            <b-badge to="/clocks" variant="danger">Clocks Info</b-badge>
            <b-form-checkbox style="color: blue"
              v-model="allSelectedClocks" :indeterminate="indeterminateClocks" aria-describedby="clocksList"
              aria-controls="clocksList" @change="toggleAllClocks" size="lg">
              {{ allSelectedClocks ? 'Un-select All' : 'Select All' }}
            </b-form-checkbox>
            <b-form-group v-slot="{ ariaDescribedby }">
              <b-form-checkbox-group
                v-model="selectedClocks"
                :options="clocksList"
                :aria-describedby="ariaDescribedby"
                name="flavour-2a"
                ref="checkClocks"
                stacked>
              </b-form-checkbox-group>
            </b-form-group>
          </div>
        </b-col>-->
      </b-row>
      <b-row><b-col>
        <b-button id="load" size="lg" variant="outline-primary"  @click="upload">Upload Dataset</b-button></b-col>
      </b-row>
      <b-row></b-row>
    </b-container>
  </div>
</template>

<script>
import { upload } from '../api'
export default {
  data () {
    return {
      errLogShow: false,
      errIdShow: false,
      errHeadShow: false,
      errPhoneShow: false,
      errAboveShow: false,
      noFileShow: false,
      errFileNameShow: false,
      errGeoIDShow: false,
      errSamIDShow: false,
      betaFile: null,
      phenoFile: null,
      dialogVisibleBeta: false,
      dialogVisiblePheno: false,
      betaProgress: 0,
      tissue: 'blood',
      ageUnit: 'Year',
      naImp: 'methyLImp',
      options: [
        { value: 'blood', text: 'Blood' },
        { value: 'saliva', text: 'Saliva' },
        { value: 'skin', text: 'Skin' },
        { value: 'brain', text: 'Brain' },
        { value: 'Breast', text: 'Breast' },
        { value: 'other', text: 'Other' }
      ],
      ageUnitOptions: [
        {value: 'Year', text: 'Year'},
        {value: 'Month', text: 'Month'},
        {value: 'Week', text: 'Week'},
        {value: 'day', text: 'day'}
      ],
      naImpOptions: [
        {value: 'methyLImp', text: 'methyLImp'}
      ],
      selectedClocks: [],
      allSelectedClocks: false,
      indeterminateClocks: false,
      clocksList: ['HorvathAge', 'Skin&BloodClock', 'ZhangBlupredAge', 'HannumAge', 'WeidnerAge', 'LinAge',
        'PedBE', 'FeSTwo', 'MEAT', 'AltumAge', 'PhenoAge', 'BNN', 'EPM', 'CorticalClock', 'VidalBraloAge', 'PerSEClock']
    }
  },
  /*watch: {
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
    }
  },    */

  methods: {
    toggleAllClocks (checked) {
      this.selectedClocks = checked ? this.clocksList.slice() : []
    },
    upload () {
      if (sessionStorage['loginState']) {
        if (this.betaFile === null || this.phenoFile === null) {
        // this.$refs['modal-nofile'].show()
          this.noFileShow = true
        } else {
          let formData = new FormData()
          let betaFile = this.$refs['beta-input'].files[0]
          let phenoFile = this.$refs['pheno-input'].files[0]
          const patBeta = /GSE[0-9]*_beta.csv/
          const patPh = /GSE[0-9]*_pheno.csv/
          if (patBeta.test(betaFile['name']) && patPh.test(phenoFile['name'])) {
            const betaID = betaFile['name'].split('_')[0]
            const phenoID = phenoFile['name'].split('_')[0]
            if (betaID === phenoID) {
              let id = Date.parse(new Date())
              id = id / 1000
              formData.append('taskID', id)
              formData.append('email', sessionStorage['email'])
              formData.append('userName', sessionStorage['name'])
              formData.append('beta', betaFile)
              formData.append('pheno', phenoFile)
              formData.append('tissue', this.tissue)
              formData.append('ageUnit', this.ageUnit)
              formData.append('imputation', this.naImp)
              formData.append('clocks', this.selectedClocks)
              console.log(formData.get('clocks'))
              sessionStorage.setItem('id', id)
              let dataName = betaFile['name'] + '  |  ' + phenoFile['name']
              sessionStorage.setItem('dataName', dataName)
              // this.$router.push({
              //   path: '/wait',
              //   name: 'Wait',
              //   params: {
              //     'id': id,
              //     'data': betaFile['name'] + phenoFile['name']
              //   }
              // })
              let config = {
                onUploadProgress: progressEvent => {
                // progressEvent.loaded:已上传文件大小
                // progressEvent.total:被上传文件的总大小
                  let percentCompleted = (progressEvent.loaded * 100) / progressEvent.total
                  this.betaProgress = percentCompleted
                  if (percentCompleted < 100) {
                    this.dialogVisibleBeta = true
                    this.dialogVisiblePheno = true
                  }
                  console.log(this.betaProgress)
                },
                header: {'Content-Type': 'multipart/form-data'}
              }
              upload(formData, config).then(res => {
                if (res.data === 'PhoneIdErr') {
                  this.errIdShow = true
                  return false
                }
                if (res.data === 'IDMismatch') {
                  this.errSamIDShow = true
                } else {
                  if (res.data === 'BetaHeadErr') {
                    this.errHeadShow = true
                  } else {
                    if (res.data === 'PhoneHeadErr') {
                      this.errPhoneShow = true
                    } else {
                      if (res.data === 'TooMuchErr') {
                        this.errAboveShow = true
                      } else {
                        console.log(res.data)
                        this.$router.push({
                          // path: '/wait',
                          name: 'Wait',
                          params: {
                            clocks: this.selectedClocks,
                            timeNeed: res.data,
                            form: formData,
                            con: config
                          }
                        })
                      }
                    }
                  }
                }
              })
            } else {
              this.errGeoIDShow = true
            }
          } else {
            this.errFileNameShow = true
          }
        }
      } else {
        this.errLogShow = true
      }
      // if (sessionStorage['loginState']) {
      //   if (this.betaFile === null || this.phenoFile === null) {
      //     // this.$refs['modal-nofile'].show()
      //     this.noFileShow = true
      //   } else {
      //     let formData = new FormData()
      //     let betaFile = this.$refs['beta-input'].files[0]
      //     let phenoFile = this.$refs['pheno-input'].files[0]
      //     let id = Date.parse(new Date())
      //     id = id / 1000
      //     formData.append('taskID', id)
      //     formData.append('email', sessionStorage['email'])
      //     formData.append('userName', sessionStorage['name'])
      //     formData.append('beta', betaFile)
      //     formData.append('pheno', phenoFile)
      //     formData.append('tissue', this.tissue)
      //     formData.append('ageUnit', this.ageUnit)
      //     formData.append('imputation', this.naImp)
      //     formData.append('clocks', this.selectedClocks)
      //     console.log(betaFile['name'])
      //     sessionStorage.setItem('id', id)
      //     let dataName = betaFile['name'] + '  |  ' + phenoFile['name']
      //     sessionStorage.setItem('dataName', dataName)
      //     this.$router.push({
      //       path: '/wait',
      //       name: 'Wait',
      //       params: {
      //         'id': id,
      //         'data': betaFile['name'] + phenoFile['name']
      //       }
      //     })
      //     let config = {
      //       onUploadProgress: progressEvent => {
      //       // progressEvent.loaded:已上传文件大小
      //       // progressEvent.total:被上传文件的总大小
      //         let percentCompleted = (progressEvent.loaded * 100) / progressEvent.total
      //         this.betaProgress = percentCompleted
      //         if (percentCompleted < 100) {
      //           this.dialogVisibleBeta = true
      //           this.dialogVisiblePheno = true
      //         }
      //         console.log(this.betaProgress)
      //       },
      //       header: {'Content-Type': 'multipart/form-data'}
      //     }
      //     upload(formData, config).then((res) => {
      //       console.log(res.data)
      //       this.$router.push({
      //         path: '/wait',
      //         name: 'Wait',
      //         params: {
      //           'id': id,
      //           'data': ''
      //         }
      //       })
      //     })
      //   }
      // } else {
      //   // this.$refs['modal-nologin'].show()
      //   this.errLogShow = true
      // }
    },
    clearFiles () {
      this.$refs['file-input'].reset()
    }
  },
  created () {
    this.value = this.$route.query.value;
    this.selectedClocks = this.value
  }
}

</script>
<style scoped>
  .upload-box{
    width: 80%;
    margin: auto;
    margin-top: 20px;
    margin-left: 20%;
  }
  .format{
    width: 20px;
    color: blue;
  }
</style>
