import {get, writable} from "svelte/store";
import {base} from "./helpers";

export const currentUrl = writable("")

function updateCurrentUrlStore() {
    const url = new URL(location.href);
    const path = url.pathname.slice(base.length)
    if (path !== get(currentUrl)) {
        currentUrl.set(path);
    }
}

// watch url for changes
export function watchUrl() {
    setInterval(() => {
        updateCurrentUrlStore()
    }, 100);
}


watchUrl()


currentUrl.subscribe(url => {
    console.log("$currentUrl changed", url);
});

