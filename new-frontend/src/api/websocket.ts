import { io } from "socket.io-client";
import { writable } from "svelte/store";
import { url } from "./rest";
import {vote} from "./stores";
import {isDevelopmentMode} from "../lib/helpers";

/**
 * Connect to backend websocket
 */
const socket = io('/', {
    path: url('/../backend/ws/socket.io'),
    transports: ['polling']
});



/**
 * Election status
 */
export enum ElectionStatus {
    ELECTIONS_NOT_STARTED = "elections_not_started",
    WAITING_FOR_NFC_TAG = "waiting_for_scan",
    TOKEN_VALID = "token_valid",
    TOKEN_NOT_VALID = "token_not_valid",
    VOTE_SUCCESS = "vote_success",
    VOTE_ERROR = "vote_error",
    DISCONNECTED = "disconnected",
}
export const electionStatus = writable(ElectionStatus.DISCONNECTED);
electionStatus.subscribe(status => {
    // if election status changes to beginning state or to one of end states, clear vote store from previous vote
    if (status === ElectionStatus.TOKEN_VALID || status === ElectionStatus.VOTE_SUCCESS || status === ElectionStatus.VOTE_ERROR || status === ElectionStatus.DISCONNECTED) {
        // @ts-ignore
        vote.reset();
    }
    console.log(`Election status changed to ${status}`);
});


/**
 * if development mode (npm run dev), set electionStatus to TOKEN_VALID for the ability to modify the app without running the backend
 */
if (isDevelopmentMode) {
    electionStatus.set(ElectionStatus.TOKEN_VALID);
}


/**
 * Tell backend that we connected to the socket (send 'join' event)
 * Then backend will send us more configuration data
 */
socket.on('connect',  () => {
    console.log('user is connected now');
    socket.emit('join', {data: 'User connected'});
});


//
// socket.on('validated_token', msg => {
//     console.log("WS validated_token", msg);
//     if (msg.data == "valid") {
//         console.log("validated_token", msg);
//         electionStatus.set(ElectionStatus.TOKEN_VALID);
//     } else if (msg.data == "invalid") {
//         electionStatus.set(ElectionStatus.TOKEN_NOT_VALID);
//     } else {
//         console.error("WS validated_token - unknown message " + msg.data);
//         electionStatus.set(ElectionStatus.TOKEN_NOT_VALID);
//     }
//
// });

/**
 * example
 * 'actual_state', {
 *    "state": state
 * }
 */
socket.on('changed_election_state', msg => {
    switch (msg.state) {
        case ElectionStatus.ELECTIONS_NOT_STARTED:
        case ElectionStatus.VOTE_ERROR:
        case ElectionStatus.VOTE_SUCCESS:
        case ElectionStatus.TOKEN_VALID:
        case ElectionStatus.WAITING_FOR_NFC_TAG:
        case ElectionStatus.TOKEN_NOT_VALID:
        case ElectionStatus.DISCONNECTED:
            electionStatus.set(msg.state);
            break;
        default:
            console.error("WS actual_state - unknown message " + msg.state);
            electionStatus.set(ElectionStatus.ELECTIONS_NOT_STARTED);
            break;
    }
    console.log("WS changed_election_state", msg);
});

/**
 * example
 * 'config', {
 *           "config": config
 *       }
 */
socket.on('config', msg => {
    console.log("TODO WS config ", msg);
});

socket.on('saving_vote_message', msg => {
    console.log("TODO WS saving_vote_message", msg);
});

export {socket};