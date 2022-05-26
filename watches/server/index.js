const express = require('express');
const app = express();
const cookieParser = require('cookie-parser');

const nonHonorsItems = [
  { title: 'Rolex', cost: 30, img: '' },
  { title: 'Omega', cost: 50, img: '' },
  { title: 'Swatch', cost: 10, img: '' },
  { title: 'Guess', cost: 2, img: '' },
  { title: 'Iwc', cost: 5, img: '' },
  {
    title: 'Tax Documents (not for fraud)',
    cost: 0,
    img: '',
  },
];

function giveItems(req, res, next) {
  // You should've gotten honors smh
  try {
    JSON.parse(req.cookies['items']);
  } catch (e) {
    res.clearCookie('items');
    res.cookie('items', JSON.stringify(nonHonorsItems), {
      sameSite: 'None',
      secure: true,
    });
  }
  next();
}

app.use(cookieParser());
app.use(
  '/',
  giveItems,
  express.static(__dirname + '/static', { extensions: ['html'] })
);

app.listen(8080);
