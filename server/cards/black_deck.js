const cards = require('./black_cards.json');

class BlackDeck {
  constructor() {
    this.cards = cards;
    this.total = this.cards.length;
    this.getCard = this.getCard.bind(this);
  }
  getCard() {
    let num = Math.floor(Math.random() * (this.total - 0));
    return this.cards[num];
  }
}

module.exports = BlackDeck;
