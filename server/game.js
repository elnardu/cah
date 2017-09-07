const WhiteDeck = require('./cards/white_deck.js');
const BlackDeck = require('./cards/black_deck.js');

const User = require('./user.js');
const uuid = require('uuid/v4');

const STAGES = {
  JOIN: 1,
  CARDS_PICK: 2,
  JUDGE_PICK: 3,
  ROUND_FINALE: 4
}

class Game {
  constructor(name, io) {
    this.whitedeck = new WhiteDeck();
    this.blackdeck = new BlackDeck();

    this.name = name;
    this.id = uuid();
    this.nsp = io.of(`/${this.id}`);

    this.stage = STAGES.JOIN;
    this.users = {};
    this.cards = [];
    this.voted = 0;
    this.judgeCounter = 0;
    this.players = 0;
    this.judge = "";
    this.blackCard = "";

    this.nsp.on('connection', (socket) => {
      console.log(`New socket connection in room /${this.id}`);
      let username;
      socket.on('join', (name) => {
        username = name;
        this.addUser(new User(name, socket.id));
        this.sendUpdates();
      });

      socket.on('card', (card) => {
        if (this.users[username].isPlaying && !this.users[username].isJudge && this.stage == STAGES.CARDS_PICK) {
          this.handleUserCard(username, card);
        } else if (this.users[username].isPlaying && this.users[username].isJudge && this.stage == STAGES.JUDGE_PICK) {
          this.triggerRoundEnd(card);
        }
      });

      socket.on('start', () => {
        if(Object.keys(this.users).length >= 3) this.roundStart();
      });

      socket.on('disconnect', () => {
        console.log("User left", username);
        this.players--;
        if(this.users[username].isJudge || this.players < 3) {
          this.clearBeforeNewRound();
          this.stage = STAGES.JOIN;
        }
        delete this.users[username];

        this.sendUpdates();
      });
    });
  }
  listUsers() {
    let data = [];
    Object.keys(this.users).forEach((user) => {
      data.push({
        name: this.users[user].name,
        isJudge: this.users[user].isJudge,
        isPlaying: this.users[user].isPlaying,
        gamesPlayed: this.users[user].gamesPlayed,
        gamesWon: this.users[user].gamesWon,
        voted: this.users[user].voted
      });
    });
    return data;
  }
  addUser(user) {
    console.log(`New user`, user.name);
    user.clear();
    user.setCards(this.whitedeck.getCards());
    this.users[user.name] = user;

  }
  roundStart() {
    this.clearBeforeNewRound();
    this.stage = STAGES.CARDS_PICK;
    Object.keys(this.users).forEach((user) => {
      this.users[user].newRound();
      while(this.users[user].cards.length < 10) {
        this.users[user].cards.push(this.whitedeck.getCard());
      }
      this.nsp.to(this.users[user].socketId).emit('whitecards', this.users[user].cards);
    });
    this.players = Object.keys(this.users).length;
    this.judgeCounter++;
    if(this.judgeCounter >= this.players) this.judgeCounter = 0;
    console.log(this.judgeCounter);
    this.judge = Object.keys(this.users)[this.judgeCounter];
    this.users[this.judge].isJudge = true;
    this.blackCard = this.blackdeck.getCard();

    this.sendUpdates();
  }
  sendUpdates() {
    this.nsp.emit('update', {
      stage: this.stage,
      cards: this.cards,
      users: this.listUsers(),
      blackCard: this.blackCard,
      winner: this.winner
    });
  }
  handleUserCard(username, card) {
    let cardNum = this.users[username].cards.indexOf(card);
    this.users[username].cards.splice(cardNum, 1);
    this.users[username].voted = true;
    this.cards.push({
      name: username,
      text: card
    });
    this.sendUpdates();
    this.voted += 1;
    if(this.voted == this.players-1) {
      this.triggerUsersVoted();
    }
  }
  triggerUsersVoted() {
    this.stage = STAGES.JUDGE_PICK;
    this.sendUpdates();
  }
  triggerRoundEnd(card) {
    if (card) {
      if(this.users[card.name]) this.users[card.name].gamesWon += 1;
      this.stage = STAGES.ROUND_FINALE;
      this.winner = card;
      this.sendUpdates();
    }
  }
  clearBeforeNewRound() {
    this.cards = [];
    this.blackCard = "";
    this.winner = {};
    this.cards = [];
    this.voted = 0;
    this.judge = "";
    this.blackCard = "";
  }
}

module.exports = Game;
