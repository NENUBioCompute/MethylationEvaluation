<template>
  <div>
    <b-navbar type="dark" variant="dark" style="height:75px">
      <b-row style="width: 100%">
        <b-col cols="9">
          <b-navbar-nav>
            <b-nav-item to="/">
              <div>
                <div style="float:left;"><img src="../../assets/sj.png" /></div>
                <div style="float:left;width:25%"><img src="../../assets/dna2.png" /></div>
              </div>
            </b-nav-item>
              <b-nav-item to="/" class="title"><b>Home</b></b-nav-item>
              <b-nav-item to="/clocks" class="title"><b>Clocks</b></b-nav-item>
              <!--<b-nav-item to="/upload" class="title"><b>Evaluation</b></b-nav-item>-->
              <b-nav-item to="/tutorials" class="title"><b>Tutorials</b></b-nav-item>
             <!--<b-nav-item to="/original" class="title"><b>OriginalMethod</b></b-nav-item>
              <b-nav-item to="/Contact" class="title"><b>Contact</b></b-nav-item>-->
              <b-nav-item to="/Contactus" class="title"><b>Q/A</b></b-nav-item>
          </b-navbar-nav>
        </b-col>
        <b-col cols="3">
          <div style="position: absolute;right: 0%;top:50%;transform: translate(-50%, -50%);">
            <b v-if="this.$store.state.nologin">
            <router-link to="/login">
              <img src="../../assets/denglu.svg" />  Login
            </router-link>
            </b>
            <b v-else style="color: #007bff">Hello, {{this.$store.state.name}}</b>
          </div>
        </b-col>
      </b-row>
  </b-navbar>
  </div>
</template>

<script>
export default {
  data () {
    return {
      logSta: this.$store.state.nologin
    }
  },
  mounted () {
  },
  methods: {
  }
}

</script>
<style scoped>
  .title{
    margin-top: 12px;
  }
</style>
