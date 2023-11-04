<template>
  <div class="body">
    <div class="header">
      <Header />
    </div>
    <div class="main">
      <router-view />
    </div>
    <div class="footer">
      <Footer />
    </div>
  </div>
</template>

<script>
import Header from './views/components/Header.vue'
import Footer from './views/components/Footer.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
export default {
  name: 'App',
  components: { Header, Footer }
}
</script>
<style>
@import './font-style/font.css';
.body{
  font-family: Gotham Bold;
  display: flex;
    flex-direction: column;
    height: 100%;
}
*{
    margin: 0;
    padding: 0;
}
html,body{
    height: 100%;
}
.header{
  flex: 0 0 60px;
}
.main{
  flex: 1 0 auto;
}
.footer{
  margin-top: 20px;
  flex: 0 0 60px;
}
</style>
