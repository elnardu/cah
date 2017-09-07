<template lang="html">
  <div class="rooms px-3">
    <h1 class="title py-3 rounded">Доступные комнаты:</h1>
    <ul class="list-group">
      <li v-for="room in rooms" class="room list-group-item justify-content-between" @click="joinRoom(room.id)">
        {{room.name}}
        <span class="badge badge-default badge-pill">{{room.players}}</span>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "rooms",
  data() {
    return {
      rooms: []
    }
  },
  created() {
    this.updateRooms()
    this.timer = setInterval(this.updateRooms, 5000)
  },
  destroyed() {
    clearInterval(this.timer)
  },
  methods: {
    joinRoom(name) {
      this.$emit('joinroom', name)
    },
    updateRooms() {
      this.$http.get('/api/list')
      .then((res) => {
        if(res.body.success) {
          this.rooms = res.body.data
        }
      })
    }
  }

}
</script>

<style lang="css" scoped>
.rooms {
  margin: 0;
}
.title {
  font-size: 2em;
  background-color: black;
  color: white;
  width: 100%;
  padding: 0.5em;
  margin-top: 0.5em;
}
.room {
  cursor: pointer;
}
</style>
