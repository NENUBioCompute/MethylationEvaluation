import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('../views/Home.vue')
    },
    {
      path: '/browse',
      name: 'Browse',
      component: () => import('../views/Browse.vue')
    },
    {
      path: '/tutorials',
      name: 'Tutorials',
      component: () => import('../views/Tutorials.vue')
    },
    {
      path: '/contact',
      name: 'Contact',
      component: () => import('../views/Contact.vue')
    },
    {
      path: '/Contactus',
      name: 'Contact',
      component: () => import('../views/Contactus.vue')
    },
    {
      path: '/clocks',
      name: 'Clocks',
      component: () => import('../views/Clocks.vue')
    },
    {
      path: '/original',
      name: 'Original',
      component: () => import('../views/Original.vue')
    },
    {
      path: '/result',
      name: 'Result',
      component: () => import('../views/result/Result.vue')
    },
    {
      path: '/upload',
      name: 'Upload',
      component: () => import('../views/Upload.vue')
    },
    {
      path: '/test',
      name: 'Test',
      component: () => import('../views/test.vue')
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('../views/login/Register.vue')
    },
    {
      path: '/registercheck',
      name: 'RegisterCheck',
      component: () => import('../views/login/RegisterCheck.vue')
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/login/Login.vue')
    },
    {
      path: '/reset',
      name: 'Reset',
      component: () => import('../views/login/RestPsw.vue')
    },
    {
      path: '/wait',
      name: 'Wait',
      component: () => import('../views/Wait.vue')
    },
    {
      path: '/404',
      name: 'page404',
      component: () => import('../views/components/404.vue')
    },
    {
      path: '*', // 页面不存在的情况下会跳到404页面
      redirect: '/404',
      name: 'notFound',
      hidden: true
    },
    {
      path: '/index',
      name: 'Index',
      component: () => import('../views/browse/Index.vue'),
      children: [
        {
          path: '/disease',
          component: () => import('../views/browse/Disease.vue')
        },
        {
          path: '/race',
          component: () => import('../views/browse/Race.vue')
        },
        {
          path: '/tissue',
          component: () => import('../views/browse/Tissue.vue')
        }
      ]
    }
  ]
})
