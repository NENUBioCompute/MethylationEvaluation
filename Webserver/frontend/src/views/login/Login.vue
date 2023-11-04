<template>
    <div class="login">
      <b-jumbotron>
      <b-container fluid>
        <b-row class="my-1">
          <b-col>
            <h1>Please LogIn</h1>
          </b-col>
        </b-row>
        <hr />
        <b-alert v-model="errorShow" variant="danger" show dismissible>Email Address or Password Error</b-alert>
        <b-row class="my-1">
          <b-col sm="3">
            <label for="input-invalid">Email</label>
          </b-col>
        </b-row>
        <b-row class="my-1">
          <b-col sm="9">
            <b-form-input id="input-invalid-email" :state="emailState" aria-describedby="input-email"
            placeholder="Your email address" v-model="email" type="email"></b-form-input>
            <b-form-invalid-feedback id="input-email">
              Please input the correct email address
            </b-form-invalid-feedback>
          </b-col>
        </b-row>
        <b-row class="my-1">
          <b-col sm="3">
            <label for="input-invalid">Password</label>
          </b-col>
        </b-row>
        <b-row class="my-1">
          <b-col sm="9">
            <b-form-input id="input-invalid-psw" :state="pswState" aria-describedby="input-psw"
            placeholder="Your password" v-model="password" type="password"></b-form-input>
            <b-form-invalid-feedback id="input-psw">
              Password cannot be empty
            </b-form-invalid-feedback>
          </b-col>
          <b-col sm="3" style="display:flex;align-content:space-around;flex-wrap:wrap">
            <router-link to="/reset"> Forget Password?</router-link>
          </b-col>
        </b-row>
        <br/>
        <b-row cols="my-1">
          <b-col sm="3">
            <b-button @click="login">Log in</b-button>
          </b-col>
        </b-row>
        <br/>
        <p>You don't have an account yet? <router-link to="/register"> Register a new account</router-link></p>
      </b-container>
    </b-jumbotron>
    </div>
  </template>

<script>
import { login } from '../../api'
export default {
  computed: {
    emailState () {
      return /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/.test(this.email)
    },
    pswState () {
      return this.password.length > 5
    }
  },
  data () {
    return {
      email: '',
      password: '',
      errorShow: false
    }
  },

  methods: {
    login () {
      // this.errorShow = false
      // if (!this.emailCheck(this.email)) {
      //   console.log('email is not correct')
      //   this.errorShow = true
      // } else if (this.email === '1') {
      //   console.log('email is empty')
      // } else {
      //   this.$router.push('/upload')
      //   sessionStorage.setItem('loginState', true)
      //   sessionStorage.setItem('email', this.email)
      // }
      let formData = new FormData()
      formData.append('email', this.email)
      formData.append('password', this.password)
      login(formData).then(res => {
        if (res.data === 'error') {
          this.errorShow = true
        } else {
          // if (location.href.indexOf('#reloaded') === -1) {
          //   location.href = location.href + '#reloaded'
          //   window.location.reload()
          // }
          this.$router.go(-1)
          this.$store.commit('setLoginState', false)
          sessionStorage.setItem('email', this.email)
          sessionStorage.setItem('name', res.data['name'])
          sessionStorage.setItem('loginState', true)
        }
      })
    }
  }
}

</script>
<style scoped>
.login{
  width: 750px;
  margin: auto;
  margin-top: 40px;
}
</style>
