const express = require('express')
const app = express()
const port = 1337

const HOST = process.env.HOST || 'electron.lol:1337'
const CHAT = process.env.CHAT || 'electron.lol:6969'

app.use(express.static('view'));

app.use(function (req, res, next) {
    res.setHeader(
      'Content-Security-Policy',
      `default-src 'none';img-src 'self'; frame-src http://${CHAT}; frame-ancestors 'none'; style-src 'self' https://cdnjs.cloudflare.com/ajax/libs/milligram/1.4.1/milligram.css https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.css https://fonts.googleapis.com/css?family=Roboto:300,300italic,700,700italic;`
    );
    next();
  });

app.get('/', (req, res) => {
  res.sendFile('index.html')
})

app.listen(port, () => {
  console.log(`Started web`)
})