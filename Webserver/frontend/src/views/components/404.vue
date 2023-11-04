<template>
  <div><h1>404 NotFound</h1></div>
</template>

<script>
export default {
  data () {
    return {
    }
  },

  created () {
    this.$emit('noLogin', false)
  }
}

</script>
<style scoped>
</style>
