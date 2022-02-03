
let port = 8079


var app = require('express')();
var cors = require('cors')
app.use(cors())
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req, res){
    //send the index.html file for all requests (not currently used)
    res.sendFile(__dirname + '/index.html');

});

http.listen(port, function(){
    console.log('listening on *:' + port);

});

const inquirer = require('inquirer');

io.on('connection', function(socket) {
    console.log("Client connected")

    socket.on("*",function(event,data) {
        console.log("event:", event, ", data:", data);
    });

    var prompt_m = function(){
        return inquirer
            .prompt([
                {type: 'list', message: 'Select action', name: 'action', choices: [
                        'scan_token_valid',
                        'scan_token_failed',
                    ]}
            ])
            .then(function({action}) {
                console.log(action)
                if (action === 'scan_token_valid') {
                    socket.emit('validated_token', { valid: 'valid'});
                }
                else if (action === 'scan_token_failed') {
                    socket.emit('validated_token', { valid: 'failed'});
                }
                else {
                    console.log('error')
                }
                prompt_m();
            });
    }
    prompt_m();
});

