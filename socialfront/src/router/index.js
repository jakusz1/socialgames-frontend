import Vue from 'vue'
import Router from 'vue-router'
import UserAuth from '@/components/UserAuth'
import Game from '@/components/Game'
import Controller from '@/components/Controller'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/games/:uri?',
      name: 'Game',
      component: Game
    },
    {
      path: '/controllers/:uri?',
      name: 'Controller',
      component: Controller
    },
    {
      path: '/auth',
      name: 'UserAuth',
      component: UserAuth
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.path === '/logout') {
    sessionStorage.removeItem('authToken')
    debugger
    next('/auth')
  } else if (sessionStorage.getItem('authToken') !== null || to.path === '/auth') {
    debugger
    next()
  } else {
    next('/auth')
  }
})

export default router
