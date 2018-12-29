<template>
  <div class="container">
    <div id="auth-container" class="row">
      <div class="col-sm-8 offset-sm-2">
        <ul class="nav nav-tabs nav-justified" id="myTab" role="tablist">
          <li class="nav-item">
            <a class="nav-link active" id="signin-tab" data-toggle="tab" href="#signin" role="tab" aria-controls="signin" aria-selected="true">{{ $t('log.in') }}</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" id="signup-tab" data-toggle="tab" href="#signup" role="tab" aria-controls="signup" aria-selected="false">{{ $t('sign.up') }}</a>
          </li>
        </ul>

        <div class="tab-content" id="myTabContent">
          <div class="tab-pane fade show active" id="signin" role="tabpanel" aria-labelledby="signin-tab">
            <form @submit.prevent="signIn">
              <div class="form-group">
                <input v-model="username" type="text" class="form-control" :placeholder="$t('username')" required>
              </div>
              <div class="form-group">
                <input v-model="password" type="password" class="form-control" :placeholder="$t('password')" required>
              </div>
              <button type="submit" class="btn btn-block btn-primary">{{ $t('log.in') }}</button>
            </form>
          </div>
          <div class="tab-pane fade" id="signup" role="tabpanel" aria-labelledby="signin-tab">
            <form @submit.prevent="signUp">
              <div class="form-group">
                <input v-model="email" type="email" class="form-control" :placeholder="$t('email')" required>
              </div>
              <div class="form-row">
                <div class="form-group col-md-6">
                  <input v-model="username" type="text" class="form-control" :placeholder="$t('username')" required>
                </div>
                <div class="form-group col-md-6">
                  <input v-model="password" type="password" class="form-control" :placeholder="$t('password')" required>
                </div>
              </div>
              <button type="submit" class="btn btn-block btn-primary">{{ $t('sign.up') }}</button>
            </form>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
const $ = window.jQuery

export default {

  data () {
    return {
      email: '', username: '', password: ''
    }
  },
  methods: {
    signUp () {
      $.post('http://localhost:8000/auth/users/create/', this.$data, (data) => {
        this.signIn()
      })
        .fail((response) => {
          alert(response.responseText)
        })
    },

    signIn () {
      const credentials = {username: this.username, password: this.password}

      $.post('http://localhost:8000/auth/token/create/', credentials, (data) => {
        sessionStorage.setItem('authToken', data.auth_token)
        sessionStorage.setItem('username', this.username)
        if (this.$route.query.from) {
          this.$router.push(this.$route.query.from)
        } else {
          this.$router.push('/games')
        }
      })
        .fail((response) => {
          alert(response.responseText)
        })
    }
  }

}
</script>

<style scoped>
  #auth-container {
    margin-top: 50px;
  }

  .tab-content {
    padding-top: 20px;
  }
</style>
