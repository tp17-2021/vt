import {io} from "socket.io-client";
import {tokenValid} from "../stores";

const socket = io('/', {
    path: '/backend/ws/socket.io',
    transports: ['polling']
});

socket.on('connect', function (event) {
    console.log('user is connected now');
    // socket.emit('client_connect_event', {data: 'User connected'});
});

socket.on('validated_token', function (msg, cb) {
    console.log("--------- validated_token", msg, cb);

    if (msg.data == "valid") {
        console.log("+++++++++++++ validated_token", msg, cb);
        tokenValid.set(true)
    } else if (msg.data == "failed") {
        tokenValid.set(false)
        // TODO: error message
    } else {
        tokenValid.set(false)
    }
});

/**
 * example
 * 'actual_state', {
 *    "state": state
 * }
 */
socket.on('actual_state', function (msg, cb) {
    console.log("--------- [TODO] actual_state ", msg, cb);
});

/**
 * example
 * 'config', {
 *           "config": config
 *       }
 */
socket.on('config', function (msg, cb) {
    console.log("--------- [TODO] config ", msg, cb);
});


// 'saving_vote_message', {
//     "data": message,
//     "message": "This message came from vote DB service"
// }
socket.on('saving_vote_message', function (msg, cb) {
    console.log("saving_vote_message", msg, cb);
});

// socket.emit('client_stop_event', {data: 'Stop doing something'});


export {socket};