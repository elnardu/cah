
class User {
  constructor(name, socketId) {
    this.name = name;
    this.socketId = socketId;
    this.gamesPlayed = 0;
    this.gamesWon = 0;

    this.cards = [];
    this.isJudge = false;
    this.isPlaying = false;
    this.voted = false;
  }
  setCards(cards) {
    this.cards = cards;
  }
  newRound() {
    this.isJudge = false;
    this.gamesPlayed += 1;
    this.isPlaying = true;
    this.voted = false;
  }
  clear() {
    this.cards = [];
    this.isJudge = false;
    this.isPlaying = false;
    this.voted = false;
  }
}

module.exports = User;
