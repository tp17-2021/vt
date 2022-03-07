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
    ELECTIONS_NOT_STARTED = "inactive",
    TOKEN_NOT_VALID = "error",
    TOKEN_VALID = "success",
    WAITING_FOR_NFC_TAG = "enabled",
    VOTE_ERROR = "vote_error",
    VOTE_SUCCESS = "vote_success",
}
export const electionStatus = writable(ElectionStatus.ELECTIONS_NOT_STARTED);
electionStatus.subscribe(status => {
    // if election status changes to beginning state or to one of end states, clear vote store from previous vote
    if (status === ElectionStatus.TOKEN_VALID || status === ElectionStatus.VOTE_SUCCESS || status === ElectionStatus.VOTE_ERROR) {
        // @ts-ignore
        vote.reset();
    }
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



socket.on('validated_token', msg => {
    console.log("WS validated_token", msg);
    if (msg.data == "valid") {
        console.log("validated_token", msg);
        electionStatus.set(ElectionStatus.TOKEN_VALID);
    } else if (msg.data == "invalid") {
        electionStatus.set(ElectionStatus.TOKEN_NOT_VALID);
    } else {
        console.error("WS validated_token - unknown message " + msg.data);
        electionStatus.set(ElectionStatus.TOKEN_NOT_VALID);
    }

});

/**
 * example
 * 'actual_state', {
 *    "state": state
 * }
 */
socket.on('actual_state', msg => {
    console.log("WS actual_state", msg);
    if (msg.state === "end" || msg.state === "inactive") {
        electionStatus.set(ElectionStatus.ELECTIONS_NOT_STARTED);
    } else if (msg.state === "start") {
        electionStatus.set(ElectionStatus.WAITING_FOR_NFC_TAG);
    } else if (msg.state === "vote_error") {
        electionStatus.set(ElectionStatus.VOTE_ERROR);
    } else if (msg.state === "vote_success") {
        electionStatus.set(ElectionStatus.VOTE_SUCCESS);
    } else {
        console.error("WS actual_state - unknown message " + msg.state);
        electionStatus.set(ElectionStatus.ELECTIONS_NOT_STARTED);
    }
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