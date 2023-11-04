<template>
  <div class="registerBox">
    <b-container fluid>
      <b-row class="my-1"><h2>Plaese Register</h2></b-row>
      <hr /><br/>
      <b-alert v-model="show" variant="danger" show dismissible>The information you entered is incorrect</b-alert>
      <b-alert v-model="showEmail" variant="danger" show dismissible>This email already exists</b-alert>
      <b-alert v-model="showCAPTCHA" variant="danger" show dismissible>CAPTCHA error</b-alert>
      <b-alert v-model="EmailChanged" variant="danger" show dismissible>Keep the email invariant please</b-alert>
      <b-row class="my-1">
        <b-col sm="3">
          <h4>Account Information</h4>
        </b-col>
        <b-col sm="9">
          <b-row class="my-1">
            <b-col>
              <label>First Name</label>
            </b-col>
          </b-row>
          <b-row class="my-1">
            <b-col sm="9">
              <b-form-input :state="fnameState" placeholder="Your First Name"
              v-model="firstName" type="text"></b-form-input>
              <b-form-invalid-feedback id="input-live-feedback">
                Please input the First Name
              </b-form-invalid-feedback>
            </b-col>
          </b-row>
          <b-row class="my-1">
            <b-col>
              <label>Last Name</label>
            </b-col>
          </b-row>
          <b-row class="my-1">
            <b-col sm="9">
              <b-form-input placeholder="Your Last Name" :state="lnameState"
              v-model="lastName" type="text"></b-form-input>
              <b-form-invalid-feedback id="input-email">
                Please input the Last Name
              </b-form-invalid-feedback>
            </b-col>
          </b-row>
          <b-row class="my-1">
            <b-col>
              <label>Institution Email (Educational emails only)</label>
            </b-col>
          </b-row>
          <b-row class="my-1">
            <b-col sm="9">
              <b-form-input :state="emailState" placeholder="Your Email Address"
              v-model="email" type="email"></b-form-input>
              <b-form-invalid-feedback id="input-email">
                Please input education email address
              </b-form-invalid-feedback>
            </b-col>
          </b-row>
          <b-button @click="check">Send CAPTCHA</b-button>
          <b-row class="my-1">
            <b-col>
              <label>Completely Automated Public Turing test to tell Computers and Humans Apart</label>
            </b-col>
          </b-row>
          <b-row class="my-1">
            <b-col sm="9">
              <b-form-input :state="CAPTCHAState" placeholder="Your CAPTCHAS"
              v-model="CAPTCHA" type="email"></b-form-input>
              <b-form-invalid-feedback id="input-email">
                Please enter 4 characters CAPTCHAS
              </b-form-invalid-feedback>
            </b-col>
          </b-row>
          <b-row class="my-1">
            <b-col sm="3">
              <label>Password</label>
            </b-col>
          </b-row>
          <b-row class="my-1">
            <b-col sm="9">
              <b-form-input :state="pswState" placeholder="Your Password"
              v-model="password" type="password"></b-form-input>
              <b-form-invalid-feedback id="input-email">
                Please input the Password
              </b-form-invalid-feedback>
            </b-col>
          </b-row>
          <b-row class="my-1">
            <b-col sm="3">
              <label>Password confirmation</label>
            </b-col>
          </b-row>
          <b-row class="my-1">
            <b-col sm="9">
              <b-form-input :state="pswConfState" placeholder="Your Password"
              v-model="confPassworrd" type="password"></b-form-input>
              <b-form-invalid-feedback id="input-email">
                Please input the Password again
              </b-form-invalid-feedback>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
      <hr /><br/>
      <b-row class="my-1">
        <b-col sm="3">
          <h4>Institution / University Information</h4>
        </b-col>
        <b-col sm="9">
          <b-row class="my-1">
            <b-col sm="3">
              <label>Institution / University</label>
            </b-col>
          </b-row>
          <b-row class="my-1">
            <b-col sm="9">
              <b-form-input :state="insNameStatee" placeholder="Your Institution or University"
              v-model="institution" type="text"></b-form-input>
              <b-form-invalid-feedback id="input-email">
                Please input the Institution or University
              </b-form-invalid-feedback>
            </b-col>
          </b-row>
          <b-row class="my-1">
            <b-col sm="3">
              <label>Country</label>
            </b-col>
          </b-row>
          <b-row class="my-1">
            <b-col sm="9">
              <b-form-input :state="countryNameState" placeholder="Your Country"
              v-model="country" type="text"></b-form-input>
              <b-form-invalid-feedback id="input-email">
                Please input the Country
              </b-form-invalid-feedback>
            </b-col>
          </b-row>
          <b-row class="my-1">
            <b-col sm="3">
              <label>Job Title / Position</label>
            </b-col>
          </b-row>
          <b-row class="my-1">
            <b-col sm="9">
              <b-form-input :state="titleNameState" placeholder="Your Title"
              v-model="title" type="text"></b-form-input>
              <b-form-invalid-feedback id="input-email">
                Please input the Job Title or Position
              </b-form-invalid-feedback>
            </b-col>
          </b-row>
          <br/>
          <b-row cols="my-1">
            <b-col sm="3">
              <b-button @click="register">Register</b-button>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import { checkEmail, register, sendEmail } from '../../api'
export default {
  computed: {
    CAPTCHAState () {
      return this.CAPTCHA.length === 4
    },
    fnameState () {
      return this.firstName.length > 0
    },
    lnameState () {
      return this.lastName.length > 0
    },
    insNameStatee () {
      return this.institution.length > 0
    },
    countryNameState () {
      return this.country.length > 0
    },
    titleNameState () {
      return this.title.length > 0
    },
    emailState () {
      return /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.edu\.cn+)+$/.test(this.email)
    },
    pswState () {
      return this.password.length > 5
    },
    pswConfState () {
      return ((this.confPassworrd === this.password) && (this.confPassworrd.length > 5))
    }
  },
  data () {
    return {
      CAPTCHA: '',
      EmailChanged: false,
      name: '',
      showCAPTCHA: false,
      answer: '',
      email: '',
      lastName: '',
      firstName: '',
      password: '',
      confPassworrd: '',
      institution: '',
      country: '',
      title: '',
      message: '',
      show: false,
      showEmail: false,
      email_checking: ''
    }
  },
  methods: {
    register () {
      if (this.firstName === '' || this.lastName === '' || this.email === '' ||
            this.country === '' || this.institution === '' || this.title === '') {
        this.show = true
        return false
      }
      if (!/^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.edu\.cn+)+$/.test(this.email)) {
        this.show = true
        return false
      }
      if (this.email_checking !== this.email) {
        this.EmailChanged = true
        return false
      }
      if (this.answer === '' || this.CAPTCHA !== this.answer) {
        this.showCAPTCHA = true
        return false
      }
      if (this.confPassworrd !== this.password || this.password.length < 5 || this.confPassworrd.length < 5) {
        this.show = true
        return false
      }
      let fdEmail = new FormData()
      console.log(this.email)
      fdEmail.append('email', this.email)
      checkEmail(fdEmail).then(res => {
        if (res.data === 'success') {
          this.showEmail = true
          return false
        } else {
          let formData = new FormData()
          formData.append('fname', this.firstName)
          formData.append('lname', this.lastName)
          formData.append('email', this.email)
          formData.append('password', this.password)
          formData.append('institution', this.institution)
          formData.append('country', this.country)
          formData.append('title', this.title)
          formData.append('status', false)
          console.log(this.email)
          register(formData).then(res => {
            if (res.data === 'success') {
              this.$router.push('/login')
            } else {
              alert('error')
            }
          })
        }
      })
    },
    check () {
      let formData = new FormData()
      this.answer = Math.floor(Math.random() * 9000 + 1000).toString()
      this.email_checking = this.email
      // formData.append('beta', '77777')
      formData.set('beta', this.answer)
      formData.set('email', this.email)
      console.log(formData.get('beta'))
      console.log(formData.get('email'))
      sendEmail(formData)
    },
    insCheck () {
      if (this.insbase.indexOf(this.institution) !== -1) {
        return true
      }
      return false
    }
  }
}
</script>
<style>
.registerBox{
  margin: auto;
  margin-top: 40px;
  width: 80%;
}
</style>
