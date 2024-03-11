import Vue from 'vue'
import Router from 'vue-router'
import UserAuth from '@/components/UserAuth'
import Game from '@/components/Game'
import TestGame from '@/components/TestGame'
import Controller from '@/components/Controller'
import Profile from '@/components/Profile'
import Main from '@/components/Main'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/games/:uri?',
      name: 'Game',
      component: Game
    },
    {
      path: '/test',
      name: 'TestGame',
      component: TestGame
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
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile
    },
    {
      path: '/',
      name: 'Main',
      component: Main
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.path === '/logout') {
    sessionStorage.removeItem('authToken')
    next('/auth')
  } else if (sessionStorage.getItem('authToken') !== null || to.path === '/auth' || to.path === '/test') {
    next()
  } else {
    next('/auth')
  }
})

export default router
