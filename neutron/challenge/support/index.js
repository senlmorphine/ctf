const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const  uuid = require('uuid4')
server.listen(6969); 

const { Server } = require("socket.io");
const io = new Server(server);

const session = require("express-session")
const path = require("path")

const ADMINU = "SHAtenDroi"
const ADMINP = "S1r1us#@3#Electron###@14343"
var bodyParser = require('body-parser')
var urlencodedParser = bodyParser.urlencoded({ extended: false })


const sessionMiddleware = session({ secret: '1Gfv%cFa^XDPjN3@Rx'});

app.use(sessionMiddleware);
app.use(express.static(path.join(__dirname, 'public'))); 
app.set('view engine', 'ejs');


io.use((socket, next) => {
  sessionMiddleware(socket.request, {}, next);
});
app.get("/", function(req, res){
    if(req.session.user){
        var username = req.session.user
        console.log(req.session)
        res.render('chat',{username:username})   
    }else{
        res.render('index')
    }
});

app.post("/", urlencodedParser, function(req, res){
    var user = req.body;
    if( user.username ===  ADMINU && user.passwd === ADMINP ){
        var username = user.username;
        req.session.user = username;
        req.session.admin = true;
        res.render('chat',{username:username})
    }
    else if( /^[a-zA-z0-9]{6,}$/.test(user.username) ){
        var username = user.username;
        req.session.user = username;
        req.session.admin = false;
        res.render('chat',{username:username});
    }
    else{
        res.send('Not valid <a href="/">go back ~~ </a>')
    }
})

io.sockets.on('connection', function (socket) {

    var msg = `You have joined ${socket.id} room`
    var reply = JSON.stringify({action: 'message', msg: msg, time:  new Date().toLocaleString()});
    socket.emit('chat', reply);
    socket.on('chat', function (data) {
        var msg = JSON.parse(data);
        var reply = JSON.stringify({action: 'message', msg: msg.msg, time:  new Date().toLocaleString()});
        var room = Array.from(socket.rooms)[0];
        io.to(room).emit('chat', reply)
    });
    socket.on('join', function(data) {
        var admin = socket.request.session['admin'];
        console.log(admin,socket.request.session)
        var room = Array.from(socket.rooms)[0];
        if(admin === true){
            var {room} = JSON.parse(data)
            socket.leave(socket.id)
            socket.join(room);
            var reply = JSON.stringify({action: 'message', msg: 'Admin joined the chat, pwn him and get the flag!!!', time:  new Date().toLocaleString()});
            io.to(room).emit('chat', reply)
        }else{
            var reply = JSON.stringify({action: 'message', msg: 'Only admin is allowed', time:  new Date().toLocaleString()});
            io.to(room).emit('chat', reply)

        }
    });

});
