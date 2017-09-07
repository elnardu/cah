<template lang="html">
  <div class="gamecontainer">
    <Rooms v-if="!inGame" @joinroom="joinRoom"/>
    <GameRoom v-else :roomId="roomId" :username="username" @exit="leaveRoom"/>
  </div>
</template>

<script>
import Rooms from './Rooms.vue'
import GameRoom from './GameRoom.vue'

export default {
  name: 'gamecontainer',
  props: ['username'],
  components: {
    Rooms,
    GameRoom
  },
  data() {
    return {
      inGame: false,
      roomId: null
    }
  },
  methods: {
    joinRoom(roomId) {
      this.inGame = true
      this.roomId = roomId
    },
    leaveRoom() {
      this.inGame = false
      this.roomId = null
    }
  }
}
</script>

<style lang="css">

</style>
