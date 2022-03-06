import {writable} from "svelte/store";

export const authenticated = writable(false)
export const pin = writable("0000")
export const jwt = writable(null)