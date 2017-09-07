const cards = require('./white_cards.json');

class WhiteDeck {
  constructor() {
    this.cards = cards;
    this.deck = cards;
    this.getCard = this.getCard.bind(this);
    this.getCards = this.getCards.bind(this);
    this.refreshCards = this.refreshCards.bind(this);
  }
  getCard() {
    if (this.cards.length == 0)
      this.refreshCards();
    let num = Math.floor(Math.random() * (this.cards.length - 0));
    let card = this.cards[num];
    this.cards.splice(num, 1);
    return card;
  }
  getCards() {
    let cards = [];
    for (var i = 0; i < 10; i++) {
      cards.push(this.getCard());
    }
    return cards;
  }
  refreshCards() {
    this.cards = this.deck;
  }
}

module.exports = WhiteDeck;
