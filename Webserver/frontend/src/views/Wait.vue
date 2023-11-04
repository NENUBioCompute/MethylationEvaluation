<template>
  <div class="waittBox">
    <b-container fluid>
      <b-row class="my-1">
        <b-col>
          <h1>Your data is being analyzed,about {{timeNeed}} min are needed, we will send you an E-mail after completed</h1>
        </b-col>
      </b-row>
      <hr />
      <div class="text-center" v-show="analysis">
        <b-spinner style="width: 5rem; height: 5rem;" label="Spinning"></b-spinner>
        <b-spinner style="width: 5rem; height: 5rem;" type="grow" label="Spinning"></b-spinner>
        <b-spinner style="width: 5rem; height: 5rem;" variant="primary" label="Spinning"></b-spinner>
        <b-spinner style="width: 5rem; height: 5rem;" variant="primary" type="grow" label="Spinning"></b-spinner>
        <b-spinner style="width: 5rem; height: 5rem;" variant="success" label="Spinning"></b-spinner>
        <b-spinner style="width: 5rem; height: 5rem;" variant="success" type="grow" label="Spinning"></b-spinner>
      </div><br/>
      <div class="text-center" v-show="!analysis">
        <b-iconstack font-scale="5">
          <b-icon stacked icon="square"></b-icon>
          <b-icon stacked icon="check"></b-icon>
        </b-iconstack>
        <b-iconstack font-scale="5">
          <b-icon stacked icon="square" variant="primary"></b-icon>
          <b-icon stacked icon="check" variant="primary"></b-icon>
        </b-iconstack>
        <b-iconstack font-scale="5">
          <b-icon stacked icon="square" variant="success"></b-icon>
          <b-icon stacked icon="check" variant="success"></b-icon>
        </b-iconstack>
      </div><br/>
      <b-row class="my-1">
        <b-col sm="2"><label class="labelFont">Task ID: </label></b-col>
        <b-col sm="3"><label class="labelFont">{{ id }}</label></b-col>
      </b-row>
      <b-row class="my-1">
        <b-col sm="2"><label class="labelFont">Your name: </label></b-col>
        <b-col sm="3"><label class="labelFont">{{ name }}</label></b-col>
      </b-row>
      <b-row class="my-1">
        <b-col sm="2"><label class="labelFont">Your email: </label></b-col>
        <b-col sm="3"><label class="labelFont">{{ email }}</label></b-col>
      </b-row>
      <b-row class="my-1">
        <b-col sm="2"><label class="labelFont">Your Data: </label></b-col>
        <b-col sm="9"><label class="labelFont"><b>{{ dataName }}</b></label></b-col>
      </b-row>
      <b-row class="my-1">
        <b-col sm="2"><label class="labelFont">Created Time: </label></b-col>
        <b-col sm="9"><label class="labelFont">{{ createTime }}</label></b-col>
      </b-row>
      <b-row class="my-1">
        <b-col sm="2"><label class="labelFont">Task  Status: </label></b-col>
        <b-col sm="3" v-show="analysis">
          <label style="font-size: 20px; color: red">In analysis</label>
          <b-spinner small label="Small Spinner"></b-spinner>
        </b-col>
        <b-col sm="3" v-show="!analysis"><label style="font-size: 20px; color: green">Completed</label></b-col>
      </b-row>
      <b-row class="my-1" v-show="!analysis">
        <b-col sm="2"><label class="labelFont">Result: </label></b-col>
        <b-col sm="5"><label class="labelFont">Results are avaible <router-link to="/result">here</router-link></label></b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { getResStatus, sendEmailend, upload_back } from '../api'
export default {
  data () {
    return {
      email: '',
      timeNeed: '',
      name: '',
      id: '',
      dataName: '',
      createTime: '',
      checkEmail: false,
      showNoEmail: false,
      showPsw: false,
      showPswLen: false,
      newPassword: '',
      newPasswordConf: '',
      analysis: true
    }
  },
  created () {
    console.log(sessionStorage['email'])
    console.log('wait')
    this.id = sessionStorage['id']
    this.timeNeed = this.$route.params.timeNeed
    this.name = sessionStorage['name']
    this.email = sessionStorage['email']
    this.dataName = sessionStorage['dataName']
    this.createTime = new Date(sessionStorage['id'] * 1000).toLocaleString().replace(/:\d{1,2}$/, ' ')
    let formData = this.$route.params.form
    let config = this.$route.params.con
    upload_back(formData, config).then(res => {
      this.analysis = false
      let formData = new FormData()
      formData.set('email', sessionStorage['email'])
      console.log(formData.get('email'))
      sendEmailend(formData)
    })
  }
}
</script>
  <style scoped>
.waittBox {
  margin: auto;
  margin-top: 40px;
  width: 70%;
}
.labelFont {
  font-size: 20px;
}
</style>
