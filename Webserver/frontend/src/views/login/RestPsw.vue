<template>
  <div class="resetBox">
    <b-container fluid>
    <b-row class="my-1">
      <b-col>
        <h1>Reset Your Password</h1>
      </b-col>
    </b-row><hr/>
    <b-alert v-model="showNoEmail" variant="danger" show dismissible>Email Address does not Exist</b-alert>
    <b-alert v-model="showPsw" variant="danger" show dismissible>Two Password do not match</b-alert>
    <b-alert v-model="showPswLen" variant="danger" show dismissible>Password is required to be at least 6 characters</b-alert>
    <b-row class="my-1">
      <b-col>
        <label for="input-invalid">Email</label>
        <b-form-input id="input-invalid-email" :state="emailState" aria-describedby="input-email"
                placeholder="Your email address" v-model="email" type="email"></b-form-input>

        <b-form-invalid-feedback id="input-email">
          Please input the correct email address
        </b-form-invalid-feedback>
      </b-col>
    </b-row>
    <br/>
    <div v-show="checkEmail">
      <b-row class="my-1"><b-col>
        <label for="input-invalid">New Password</label>
        <b-form-input id="input-invalid-password" :state="newPswState"
                placeholder="Your New Password" v-model="newPassword" type="password"></b-form-input>

        <b-form-invalid-feedback id="input-psw">
          Your password is required to be at least 6 characters
        </b-form-invalid-feedback>
      </b-col></b-row>
      <br/>
      <b-row class="my-1"><b-col>
        <label for="input-invalid">New Password Confirmation</label>
        <b-form-input id="input-invalid-password-conf" :state="newPswConfState"
                placeholder="New Password Confirmation" v-model="newPasswordConf" type="password"></b-form-input>

        <b-form-invalid-feedback id="input-psw-conf">
          Your confirmation password do not match
        </b-form-invalid-feedback>
      </b-col></b-row>
      <br/>
      <b-row class="my-1"><b-col>
          <b-button @click="reset">Reset Password</b-button>
      </b-col></b-row>
    </div>
    <b-row v-show="!checkEmail" class="my-1">
      <b-col sm="3">
        <b-button @click="check">Reset Password</b-button>
      </b-col>
    </b-row>
  </b-container>
  <b-modal id="modal-reset" hide-footer title="BootstrapVue">
    <div class="d-block text-center">
      <h3>Hello From This Modal!</h3>
    </div>
    <b-button class="mt-3" block @click="toLogin">To Login</b-button>
  </b-modal>
  </div>
</template>

<script>
import { checkEmail, resetPsw } from '../../api'
export default {
  data () {
    return {
      email: '',
      checkEmail: false,
      showNoEmail: false,
      showPsw: false,
      showPswLen: false,
      newPassword: '',
      newPasswordConf: ''
    }
  },
  computed: {
    emailState () {
      return /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/.test(this.email)
    },
    newPswState () {
      return this.newPassword.length > 5
    },
    newPswConfState () {
      return ((this.newPasswordConf === this.newPassword) && (this.newPasswordConf.length > 5))
    }
  },
  methods: {
    check () {
      let formData = new FormData()
      formData.append('email', this.email)
      checkEmail(formData).then(res => {
        if (res.data === 'success') {
          this.checkEmail = true
          this.showNoEmail = false
        } else {
          this.showNoEmail = true
        }
      })
      // if (this.email === 'zongxizeng@gmail.com') {
      //   this.checkEmail = true
      //   this.showNoEmail = false
      // } else {
      //   this.showNoEmail = true
      // }
    },
    reset () {
      let formData = new FormData()
      formData.append('email', this.email)
      if (this.newPassword.length < 6 || this.newPasswordConf < 6) {
        this.showPswLen = true
      }
      if (this.newPasswordConf !== this.newPassword) {
        this.showPsw = true
      } else {
        formData.append('password', this.newPassword)
        resetPsw(formData).then(res => {
          console.log(res.data)
          if (res.data === 'success') {
            this.showPsw = false
            this.showPswLen = false
            this.$bvModal.show('modal-reset')
          } else {
            this.showPsw = true
          }
        })
      }
    },
    toLogin () {
      this.$bvModal.hide('modal-reset')
      this.$router.push('/login')
    }
  }
}

</script>
<style scoped>
.resetBox{
  margin: auto;
  margin-top: 40px;
  width: 50%;
}
</style>
