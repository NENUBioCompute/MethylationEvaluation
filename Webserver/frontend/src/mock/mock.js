import Mock from 'mockjs' // es6语法引入mock模块
Mock.mock('/login', { // 输出数据
  'name': '@name' // 随机生成姓名
  // 还可以自定义其他数据
})
Mock.mock('/list', { // 输出数据
  'age|10-20': 10
  // 还可以自定义其他数据
})
Mock.mock('/getid', 'post', function (option) {
  var $id = JSON.parse(option.body).id
  if ($id) {
    return Mock.mock({
      status: 200,
      message: '提交成功！！！'
    })
  } else {
    return Mock.mock({
      status: 400,
      message: '未提交参数'
    })
  }
})
