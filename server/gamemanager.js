const Game = require('./game.js');


class GameManager {
  constructor(io) {
    this.games = {};
    this.io = io;
  }
  createGame(name) {
    return new Promise((resolve, reject) => {
      if(this.listOfGames().indexOf(name) != -1) {
        reject("Уже есть комната с таким именем");
      } else {
        var game = new Game(name, this.io);
        this.games[name] = game;
        resolve();
      }
    });
  }
  listOfGames() {
    let data = [];
    Object.keys(this.games).forEach((game) => {
      data.push({
        players: this.games[game].listUsers().length,
        name: this.games[game].name,
        id: this.games[game].id
      });
    });
    return data;
  }
}

module.exports = GameManager;
