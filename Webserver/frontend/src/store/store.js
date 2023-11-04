import Vue from 'vue'

import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    // 定义一个name，以供全局使用
    name: 'Xizeng Zong',
    nologin: true,
    datasts: [],
    clockList: [],
    model: 'datasets'
  },
  mutations: {
    setLoginState (state, isLogin) { // 上传登录状态
      state.nologin = isLogin
    },
    setDatastsState (state, data) { // 上传表格选中的数据
      state.datasts = data
    },
    setClockListState (state, clocks) { // 上传表格选中的时钟信息
      state.clockList = clocks
    },
    setModelState (state, model) { // 上传表格选中的模式，数据集、疾病、组织、种族
      state.model = model
    }
  }
})

export default store
