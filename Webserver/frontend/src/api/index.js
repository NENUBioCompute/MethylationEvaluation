import axios from 'axios'

if (process.env.NODE_ENV === 'development') {
  axios.defaults.baseURL = 'http://47.99.71.176:8808'
} else if (process.env.NODE_ENV === 'debug') {
  axios.defaults.baseURL = 'http://47.99.71.176:8808'
} else if (process.env.NODE_ENV === 'production') {
  axios.defaults.baseURL = 'http://47.99.71.176:8808'
}

const backUrl = axios.defaults.baseURL

export function uploadStructure (data) {
  return axios({
    method: 'post',
    data: {data: data},
    url: backUrl + '/api/upload_structure'
  })
}

// 上传文件
export function upload (formData, config) {
  return axios({
    method: 'post',
    data: formData,
    url: backUrl + '/api/upload',
    config: config
  })
}

export function upload_back (formData, config) {
  return axios({
    method: 'post',
    data: formData,
    url: backUrl + '/api/upload_back',
    config: config
  })
}

// 登录
export function login (formData) {
  return axios({
    method: 'post',
    data: formData,
    url: backUrl + '/api/login'
  })
}

// 注册
export function register (formData) {
  return axios({
    method: 'post',
    data: formData,
    url: backUrl + '/api/register'
  })
}
// 验证邮箱
export function checkEmail (formData) {
  return axios({
    method: 'post',
    data: formData,
    url: backUrl + '/api/checkEmail'
  })
}
export function sendEmail (formData) {
  return axios({
    method: 'post',
    data: formData,
    url: backUrl + '/api/email_che'
  })
}
export function sendEmailend (formData) {
  return axios({
    method: 'post',
    data: formData,
    url: backUrl + '/api/email_send'
  })
}
// 修改密码
export function resetPsw (formData) {
  return axios({
    method: 'post',
    data: formData,
    url: backUrl + '/api/resetPsw'
  })
}
// 下载结果

// 获取数据集
export function getDatasets () {
  return axios({
    method: 'get',
    url: backUrl + '/api/dataset'
  })
}

// 获取疾病数据
export function getDisease () {
  return axios({
    method: 'get',
    url: backUrl + '/api/disease'
  })
}
// 获取组织数据
export function getTissue () {
  return axios({
    method: 'get',
    url: backUrl + '/api/tissue'
  })
}
// 获取种族数据
export function getRace () {
  return axios({
    method: 'get',
    url: backUrl + '/api/race'
  })
}

// 获取时钟信息
export function getClocks () {
  return axios({
    method: 'get',
    url: backUrl + '/api/clocks'
  })
}

// 获取结果状态
export function getResStatus () {
  return axios({
    method: 'get',
    url: backUrl + '/api/resStatus'
  })
}

// 读取
export function readme () {
  return axios({
    method: 'get',
    url: 'http://localhost:8809/static/Tutorials.md'
  })
}
