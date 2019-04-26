import VueI18n from 'vue-i18n'
import Vue from 'vue'
import en from '@/lang/en.json'
import pl from '@/lang/pl.json'

Vue.use(VueI18n)
export const i18n = new VueI18n({
  locale: 'pl', // set locale
  fallbackLocale: 'en',
  messages: { en, pl }// set locale messages
})
