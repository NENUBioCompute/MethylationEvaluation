<template>
  <div>
    <b-container>
    <!-- Ignored the float, just lazy design -->
    <!-- <b-btn class="float-right"
           :disabled="selectedRows.length === 0"
           @click="clearSelected">
      Clear selection
    </b-btn> -->
    <b-pagination :per-page="perPage" v-model="currentPage" :total-rows="items.length"></b-pagination>
    Amount of items selected: {{ selectedRows.length }}
    <b-table :items="items" :fields="fields" :per-page="perPage" :current-page="currentPage"
    @row-clicked="rowClicked" :tbody-tr-class="tbodyRowClass" primary-key="id">
      <template v-slot:cell(selected)="{ item, field: { key } }" >
        <b-checkbox v-model="item[key]"></b-checkbox>
      </template>
    </b-table>
  </b-container>
  </div>
</template>

<script>
export default {
  computed: {
    selectedRows () {
      return this.items.filter(item => item.selected)
    }
  },
  data () {
    return {
      fields: [
        { key: 'selected' },
        { key: 'id', sortable: true }
      ],
      items: [],
      perPage: 50,
      currentPage: 1
    }
  },
  methods: {
    // clearSelected () {
    //   this.selectedRows.forEach((item) => {
    //     this.$delete(item, 'selected')
    //   })
    // },
    tbodyRowClass (item) {
      /* Style the row as needed */
      if (item.selected) {
        return ['b-table-row-selected', 'table-primary', 'cursor-pointer']
      } else {
        return ['cursor-pointer']
      }
    },
    rowClicked (item) {
      if (item.selected) {
        this.$set(item, 'selected', false)
      } else {
        this.$set(item, 'selected', true)
      }
    }
  },
  created () {
    for (let i = 1; i < 5000; i++) {
      this.items.push({ id: i })
    }
  }
}

</script>
<style scoped>
</style>
