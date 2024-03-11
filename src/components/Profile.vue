<template>
  <div class="container my-auto">
    <div class="card bg-light text-left">
      <div class="card-header">
        {{$t('profile.header')}}
      </div>
    <div v-if="edit_mode" class="card-body">
      <form v-on:submit.prevent>
        <div class="form-group row">
          <label for="username" class="col-sm-2 col-form-label">{{$t('username')}}</label>
          <div class="col-sm-10">
            <input type="text" class="form-control" id="username" v-model="new_username">
          </div>
        </div>
        <div class="form-group row">
          <label for="email" class="col-sm-2 col-form-label">{{$t('email')}}</label>
          <div class="col-sm-10">
            <input type="text" class="form-control" id="email" v-model="new_email">
          </div>
        </div>
      </form>
      <button v-on:click="discard()" class="btn btn-block btn-secondary">{{ $t('discard') }}</button>
      <button v-on:click="save()" class="btn btn-block btn-success">{{ $t('save') }}</button>
    </div>
    <div v-else class="card-body">
      <form>
        <div class="form-group row">
          <label for="staticUsername" class="col-sm-2 col-form-label">{{$t('username')}}</label>
          <div class="col-sm-10">
            <input type="text" readonly class="form-control-plaintext" id="staticUsername" v-model="username">
          </div>
        </div>
        <div class="form-group row">
          <label for="staticEmail" class="col-sm-2 col-form-label">{{$t('email')}}</label>
          <div class="col-sm-10">
            <input type="text" readonly class="form-control-plaintext" id="staticEmail" v-model="email">
          </div>
        </div>
      <div class="form-group row">
          <label for="staticWon" class="col-sm-2 col-form-label">{{$t('total_won')}}</label>
          <div class="col-sm-10">
            <input type="number" readonly class="form-control-plaintext" id="staticWon" v-model="total_won">
          </div>
        </div>
      <div class="form-group row">
          <label for="staticScore" class="col-sm-2 col-form-label">{{$t('total_score')}}</label>
          <div class="col-sm-10">
            <input type="number" readonly class="form-control-plaintext" id="staticScore" v-model="total_score">
          </div>
        </div>
      </form>
      <button class="btn btn-secondary btn-block" @click='editMode()'>{{$t('profile.edit')}}</button>
    </div>
    </div>
  </div>
</template>

<script>
const $ = window.jQuery

export default {
  name: 'Profile',
  data () {
    return {
      username: '',
      email: '',
      total_won: 0,
      total_score: 0,
      edit_mode: false,
      new_username: '',
      new_email: ''
    }
  },
  created () {
    $.ajaxSetup({
      headers: {
        'Authorization': `Token ${sessionStorage.getItem('authToken')}`
      }
    })
    $.get(`http://${this.$backend}/api/user/`, (data) => {
      this.username = data.username
      this.email = data.email
      this.total_won = data.total_won
      this.total_score = data.total_score
      sessionStorage.setItem('username', this.username)
    }).fail((response) => {
      alert(response.responseText)
    })
  },
  methods: {
    editMode () {
      this.new_username = this.username
      this.new_email = this.email
      this.edit_mode = true
    },
    save () {
      $.post(`http://${this.$backend}/api/user/`, {username: this.new_username, email: this.new_email}, (data) => {
        this.username = data.username
        this.email = data.email
        sessionStorage.setItem('username', this.username)
      })
        .fail((response) => {
          alert(response.responseText)
        })
      this.edit_mode = false
    },
    discard () {
      this.edit_mode = false
    }
  }
  // watch: {
  //   username: function (val) {
  //     this.new_username = val
  //   },
  //   email: function (val) {
  //     this.new_email = val
  //   }
  // }
}
</script>
