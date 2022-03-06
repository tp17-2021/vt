import { io } from "socket.io-client";
import { readable, writable } from "svelte/store";
// import {url} from "./api";

export enum ElectionStatus {
    ELECTIONS_NOT_STARTED = "disabled",
    TOKEN_NOT_VALID = "error",
    TOKEN_VALID = "success",
    WAITING_FOR_NFC_TAG = "enabled",
}

export const electionStatus = writable(ElectionStatus.TOKEN_VALID);