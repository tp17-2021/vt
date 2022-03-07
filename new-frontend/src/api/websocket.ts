import { io } from "socket.io-client";
import { readable, writable } from "svelte/store";
import { url } from "./rest";
import {vote} from "./stores";
// import {url} from "./api";

export enum ElectionStatus {
    ELECTIONS_NOT_STARTED = "inactive",
    TOKEN_NOT_VALID = "error",
    TOKEN_VALID = "success",
    WAITING_FOR_NFC_TAG = "enabled",
    VOTE_ERROR = "vote_error",
    VOTE_SUCCESS = "vote_success",
}

export const electionStatus = writable(ElectionStatus.ELECTIONS_NOT_STARTED);

electionStatus.subscribe(status => {
    // if election status changes to TOKEN_VALID, clear vote store from previous vote
    if (status === ElectionStatus.TOKEN_VALID) {
        // @ts-ignore
        vote.reset();
    }
});

// if development, set electionStatus to TOKEN_VALID for the ability to modify the app without docker
if (process.env.NODE_ENV === "development") {
    electionStatus.set(ElectionStatus.TOKEN_VALID);
}


const socket = io('/', {
    path: url('/../backend/ws/socket.io'),
    transports: ['polling']
});



socket.on('connect', function (event) {
    console.log('user is connected now');
    socket.emit('join', {data: 'User connected'});
});

socket.on('validated_token', function (msg, cb) {
    console.log("WS avalidated_token", msg, cb);
    if (msg.data == "valid") {
        console.log("+++++++++++++ validated_token", msg, cb);
        electionStatus.set(ElectionStatus.TOKEN_VALID);
    } else if (msg.data == "invalid") {
        electionStatus.set(ElectionStatus.TOKEN_NOT_VALID);
    } else {
        alert("WS validated_token - unknown message " + msg.data);
        electionStatus.set(ElectionStatus.TOKEN_NOT_VALID);
    }

});

/**
 * example
 * 'actual_state', {
 *    "state": state
 * }
 */
socket.on('actual_state', function (msg, cb) {
    console.log("WS actual_state", msg, cb);
    if (msg.state === "end" || msg.state === "inactive") {
        electionStatus.set(ElectionStatus.ELECTIONS_NOT_STARTED);
    } else if (msg.state === "start") {
        electionStatus.set(ElectionStatus.WAITING_FOR_NFC_TAG);
    } else if (msg.state === "vote_error") {
        electionStatus.set(ElectionStatus.VOTE_ERROR);
    } else if (msg.state === "vote_success") {
        electionStatus.set(ElectionStatus.VOTE_SUCCESS);
    } else {
        alert("WS actual_state - unknown message " + msg.state);
        electionStatus.set(ElectionStatus.ELECTIONS_NOT_STARTED);
    }
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