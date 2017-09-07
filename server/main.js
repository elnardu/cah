const express = require('express'),
  app = express(),
  http = require('http').Server(app),
  io = require('socket.io')(http),
  port = 3000,
  path = require('path'),
  morgan = require('morgan'),
  bodyParser = require('body-parser'),
  GameManager = require('./gamemanager.js');

app.use(express.static(path.resolve(__dirname + '/../client/dist')));
// app.get('/', (req, res) => {
//   res.redirect('/index.html');
// });

app.use(morgan('dev'));
app.use(bodyParser.json());

gameManager = new GameManager(io);
gameManager.createGame("Test Room");
// gameManager.createGame("Test Room 2");
// gameManager.createGame("Test Room 3");



app.get('/api/list', (req, res) => {
  res.json({
    success: true,
    data: gameManager.listOfGames()
  });
});

app.get('/api/create', (req, res) => {
  let name = req.body.name;
  if(!name) {
    res.json({
      success: false,
      error: "Необходимо ввести название комнаты!"
    });
    return;
  }

  gameManager.createGame(name).then(() => {
    res.json({success: true});
  });
});



http.listen(port, () => console.log('listening on port ' + port));
