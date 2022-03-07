import {get, writable} from "svelte/store";

const base = (import.meta.env.VITE_BASE_PATH ?? "");
console.log("base", base);


export const currentUrl = writable("")

function updateUrl() {
    const url = new URL(location.href);
    const path = url.pathname.slice(base.length)
    if (path !== get(currentUrl)) {
        currentUrl.set(path);
    }
}

// watch url for changes
export function watchUrl() {
    setInterval(() => {
        updateUrl()
    }, 100);
}


watchUrl()


currentUrl.subscribe(url => {
    console.log("currentUrl changed", url);
});