<template>
<div>
    <b-jumbotron style="background: #eeeeee; height: 360px; text-align: center; padding-top: 45px;"
    header="BootstrapVue" lead="Bootstrap v4 Components for Vue.js 2">
    <p>For more information visit website</p>
    <hr class="my-4">
    <b-button variant="primary" href="#" size="lg">Do Something</b-button>
    <b-button variant="success" href="#" size="lg">Do Something Else</b-button>
  </b-jumbotron>
  <div class="container">
      <!-- Example row of columns -->
      <div class="row">
        <div class="col-md-4">
          <h2>Heading</h2>
          <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
        </div>
        <div class="col-md-4">
          <h2>Heading</h2>
          <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
       </div>
        <div class="col-md-4">
          <h2>Heading</h2>
          <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
        </div>
      </div>
    </div> <!-- /container -->
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
