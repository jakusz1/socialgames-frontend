<template>
  <div class="locale-changer mr-2">
    <select v-model="$i18n.locale" class="form-control">
      <option v-for="(lang, i) in langs" :key="`Lang${i}`" :value="lang">{{ lang }}</option>
    </select>
  </div>
</template>

<script>
export default {
  name: 'LocaleChanger',
  data () {
    return { langs: ['en', 'pl'] }
  }
}
</script>
