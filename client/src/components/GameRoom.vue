<template lang="html">
  <div class="gameroom" id="gameroom">
    <!-- topbuttons -->
    <div class="w-100 mt-3 d-flex justify-content-between">
      <button type="button" name="button" class="black-button rounded-right" @click="exit">Выйти</button>
      <button type="button" name="button" class="black-button rounded" @click="toggleFullScreen">Полный экран</button>
      <button type="button" name="button" class="black-button rounded-left" @click="toggleUsermenu">Игроки</button>
    </div>

    <!-- users list and stats -->
    <div class="usersmenu" :class="{toggled: usersMenuToggled}">
      <div class="d-flex justify-content-end">
        <button type="button" name="button" class="usersmenu-closebutton py-3" @click="toggleUsermenu">Закрыть</button>
      </div>
      <ul class="list-group mt-4">
        <li v-for="user in users" class="list-group-item justify-content-between" :class="{'list-group-item-warning': !user.isPlaying, 'list-group-item-success': user.voted, 'list-group-item-info': user.isJudge}">
          {{user.name}}
          <div>
            <span class="badge badge-success badge-pill">{{user.gamesWon}}</span>
          </div>
        </li>
      </ul>
    </div>

    <!-- display winner -->
    <div v-if="stage == STAGES.ROUND_FINALE" class="winnerdisplay d-flex flex-column justify-content-center align-items-center">
      <h2>Победу одержал</h2>
      <h1 class="text-success">{{winner.name}}</h1>
    </div>

    <!-- display prepare info -->
    <div v-if="stage == STAGES.JOIN || stage == STAGES.ROUND_FINALE" class="roundprepare d-flex flex-column justify-content-center align-items-center">
      <h2>Ожидаем игроков</h2>
      <p class="text-muted">необходимо минимум 3 игрока для старта</p>
      <button v-if="users.length >= 3" type="button" name="button" class="btn btn-success" @click="startRound">Начать</button>
    </div>



    <!-- blackcard -->
    <div v-if="stage == STAGES.CARDS_PICK || stage == STAGES.JUDGE_PICK" class="blackcard rounded" lang="ru">{{blackCard}}</div>

    <p>{{info}}</p>

    <!-- <p :class="{judge: isJudge}">{{info}}</p> -->

    <!-- whitedeck -->
    <div v-if="!me.isJudge && !voted && me.isPlaying && stage != STAGES.JOIN && stage != STAGES.ROUND_FINALE" class="deck">
      <div v-for="card in whiteCards" class="deck-card rounded-top" lang="ru" @click="handleCardClick(card)">
        {{card}}
      </div>
    </div>

    <!-- choosen cards deck -->
    <div v-if="(me.isJudge || voted || !me.isPlaying) && stage != STAGES.ROUND_FINALE" class="deck">
      <div v-for="card in cards" class="deck-card rounded-top" lang="ru" @click="handleCardClick(card)">
        {{card.text}}
      </div>
    </div>

    <!-- winner card -->
    <div v-if="stage == STAGES.ROUND_FINALE" class="deck justify-content-center">
      <div class="deck-blackcard rounded-top" lang="ru">
        {{blackCard}}
      </div>
      <div class="deck-card rounded-top" lang="ru">
        {{winner.text}}
      </div>
    </div>


  </div>
</template>

<script>
import io from 'socket.io-client'

const STAGES = {
  JOIN: 1,
  CARDS_PICK: 2,
  JUDGE_PICK: 3,
  ROUND_FINALE: 4
}

export default {
  name: "gameroom",
  props: ['roomId', 'username'],
  data() {
    return {
      me: {},
      whiteCards: [
        "ЭТО КАРТА",
        "ЭТО КАРТА",
        "ЭТО КАРТА",
        "ЭТО КАРТА",
        "ЭТО КАРТА",
        "ЭТО КАРТА",
        "ЭТО КАРТА",
        "ЭТО неКАРТА",
        "ЭТО КАРТА"
      ],
      blackCard: "Надеюсь в моем китайском блюде мне не попадется",
      cards: [],
      users: [],
      usersMenuToggled: false,
      fullscreenToggled: false,

      info: "",
      stage: 0,
      voted: false,
      winner: "",

      STAGES: STAGES
    }
  },
  created() {
    this.socket = io(`/${this.roomId}`)
    console.log(this.socket);
    this.socket.emit('join', this.username)

    this.socket.on('update', data => {
      console.log(data);
      this.stage = data.stage
      this.users = data.users
      this.blackCard = data.blackCard
      this.users.forEach(user => {
        if(user.name == this.username) this.me = user
      })
      this.cards = data.cards
      this.winner = data.winner
    })

    this.socket.on('whitecards', whiteCards => {
      this.whiteCards = whiteCards
    })

  },
  destroyed() {
    this.socket.disconnect();
  },
  methods: {
    toggleUsermenu() {
      this.usersMenuToggled = !this.usersMenuToggled
    },
    toggleFullScreen() {
      if (this.fullscreenToggled) {
        if (document.cancelFullScreen) {
          document.cancelFullScreen();
        } else if (document.mozCancelFullScreen) {
          document.mozCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
          document.webkitCancelFullScreen();
        }
        this.fullscreenToggled = false
      } else {
        let elem = document.getElementById('gameroom');
        if (elem.requestFullscreen) {
          elem.requestFullscreen();
        } else if (elem.mozRequestFullScreen) {
          elem.mozRequestFullScreen();
        } else if (elem.webkitRequestFullscreen) {
          elem.webkitRequestFullscreen();
        }
        this.fullscreenToggled = true
      }
    },
    exit() {
      this.$emit('exit')
    },
    startRound() {
      this.socket.emit('start')
    },
    handleCardClick(card) {
      if (this.stage == this.STAGES.CARDS_PICK && !this.me.isJudge && this.me.isPlaying && !this.voted) {
        this.socket.emit('card', card)
        this.voted = true
        this.info = "Карты игроков:"
      } else if (this.stage == this.STAGES.JUDGE_PICK && this.me.isJudge && this.me.isPlaying) {
        this.socket.emit('card', card)
      }
    }
  },
  watch: {
    stage() {
      if(this.stage == this.STAGES.JOIN) {
        this.info = ""
      } else if (this.stage == this.STAGES.CARDS_PICK) {
        if (this.me.isJudge) this.info = "Ты выбран судьей. Дождись выбора остальных"

      } else if (this.stage == this.STAGES.JUDGE_PICK) {
        if (this.me.isJudge) this.info = "Ты выбран судьей. Выбери самый смешной вариант"
        else this.info = "Ждем выбора судьи"

      } else if (this.stage == this.STAGES.ROUND_FINALE) {
        this.info = ""
        this.voted = false
      }
    }
  }
}
</script>

<style lang="css">
.gameroom {
  width: 100%;
  height: 100vh;
  margin: 0;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.usersmenu {
  width: 100%;
  height: 100vh;
  position: absolute;
  margin: 0;
  top: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7);
  padding: 1em;
  transition: all ease 0.5s;
  opacity: 0;
  z-index: -100;
}

.toggled {
  opacity: 1;
  z-index: 1;
}

.usersmenu-closebutton {
  color: white;
  border: none;
  background: transparent;
}

.black-button {
  background: black;
  color: white;
  padding: 1em;
  border: none;
  z-index: 0;
}

.blackcard {
  width: 60%;
  color: white;
  background: black;
  padding: 1em 0.5em;
  height: 50%;
  font-weight: bold;
  font-size: 1.6em;
  hyphens: auto;
}

.deck {
  z-index: 0;
  height: 30%;
  width: 100%;
  overflow-x: scroll;
  margin: 0;

  display: flex;
  flex-direction: row;
}

.deck-card {
  z-index: 0;
  height: 100%;
  margin: 0;
  min-width: 9em;
  max-width: 9em;
  padding: 0.5em;
  color: black;
  border: solid 1px black;
  border-bottom: none;
  font-weight: bold;
  font-size: 1.2em;
  margin-right: 5px;
  hyphens: auto;
  cursor: pointer;
}

.deck-blackcard {
  background: black;
  color: white;
  z-index: 0;
  height: 100%;
  margin: 0;
  min-width: 9em;
  max-width: 9em;
  padding: 0.5em;
  border: solid 1px black;
  border-bottom: none;
  font-weight: bold;
  font-size: 1.2em;
  margin-right: 5px;
  hyphens: auto;
  cursor: pointer;
}

.judge {
  color: red;
}

.largedisplay {
  font-weight: bold;
  font-size: 2em;
  color: black;
}


</style>
