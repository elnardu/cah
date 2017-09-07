<template>
  <div id="app" class="">
    <Login v-if="!isLogged" @login="login"/>
    <GameContainer :username="username" v-else />
  </div>
</template>

<script>
import Login from './components/Login'
import GameContainer from './components/GameContainer'
import io from 'socket.io-client'

export default {
  name: 'app',
  components: {
    Login,
    GameContainer
  },
  data() {
    return {
      username: "",
      isLogged: false
    }
  },
  mounted() {
    window.test = this
  },
  methods: {
    login(username) {
      this.username = username
      this.isLogged = true
    }
  }
}
</script>

<style>
body, html, #app {
  width: 100vw;
  height: 100vh;
  margin: 0;
  overflow: hidden;

}
</style>
