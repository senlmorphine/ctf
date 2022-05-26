const db = require('better-sqlite3')('db/database.db')
const crypto = require('crypto')

db.exec('DROP TABLE IF EXISTS riot; CREATE TABLE riot (profile_id TEXT, name TEXT, score INT);')

const names = ['Viper', 'Jett', 'Yoru', 'Reyna']
const user = () => crypto.randomBytes(8).toString('hex')
const score = () => Math.round(Math.random() * 100)
const insert = db.prepare('INSERT INTO riot (profile_id, name, score) VALUES (?, ?, ?)');
insert.run(user(), 'eldiablo', -32)
for (let name of names) {
    insert.run(user(), name, score())
}

module.exports = db;
