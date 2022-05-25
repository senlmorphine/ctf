const express = require('express');
const session = require('express-session');
const fs = require('fs');

const app = express();

const skins = require('./inventory.json');

const skin = {
    name: 'some skin',
    price: 0.25,
    description: 'a skin',
    quantity: 1
};

skins['grass'] = {
    name: 'grass',
    price: 2.5e+25,
    description: fs.readFileSync('flag.txt', 'utf8').trim(),
    quantity: 1
};

app.use(express.json({ extended: true }));

app.set('view engine', 'ejs');

app.use(session({
    secret: require('crypto').randomBytes(64).toString('hex'),
    resave: false,
    saveUninitialized: true,
}));

app.use((req, res, next) => {
    if (req.session.money !== undefined)
        return next();

    req.session.money = 5;

    if (req.ip == '127.0.0.1') {
        req.session.admin = true;
    }

    next();
});

app.get('/', (req, res) => {
    res.render('index', { skins, money: req.session.money });
});

app.post('/api/v1/sell', (req, res) => {
    for (const [key, value] of Object.entries(req.body)) {
        if (key === 'grass' && !req.session.admin) {
            continue;
        }

        if (!skins[key]) {
            skins[key] = JSON.parse(JSON.stringify(skin));
        }

        for (const [k, v] of Object.entries(value)) {
            if (k === 'quantity') {
                skins[key][k] += v;
            } else {
                skins[key][k] = v;
            }
        }
    }

    res.send('Sell successful');
});

app.post('/api/v1/buy', (req, res) => {
    const { skin, quantity } = req.body;

    if (typeof skin === 'undefined' || typeof quantity !== 'number' || quantity <= 0 || !skins[skin]) {
        return res.status(400).send('Invalid request');
    }

    if (skins[skin].quantity >= quantity) {
        if (req.session.money >= skins[skin].price * quantity) {
            skins[skin].quantity -= quantity;
            req.session.money -= skins[skin].price * quantity;
            res.json(skins[skin]);
        } else {
            res.status(402).send('Not enough money');
        }
    } else {
        res.status(451).send('Not enough skin');
    }
});

app.post('/api/v1/money', (req, res) => {
    if (req.session.admin) {
        req.session.money += req.body.money;
        res.send('Money added');
    } else {
        res.status(403).send('Not admin');
    }
});

app.listen(3000, () => {
    console.log('Listening on port 3000');
});
