import axios from "axios";
import {configLoaded, parties, texts, vote} from "./stores";
import {get} from "svelte/store";

// TODO: temporary solution, will call real api in the future
const base = (import.meta.env.VITE_BASE_PATH ?? "");
console.log("base", base);

export function url(path: string) {
    return `${base}${path}`;
}

export async function loadConfig()
{
    try {
        let response = await axios.get(url("/config_files/config.json"));
        return response.data;
    } catch (error) {
        console.error("vyskytla sa chyba getConfig(): " + JSON.stringify(error, null, 2) );
        return null;
    }
}

loadConfig().then(data => {
    console.log("config data", data);
    parties.set(data.parties);
    texts.set(data.texts);
    configLoaded.set(true);
});


export async function sendVoteParliament()
{
    try {
        let response = await axios.post(url("/../backend/api/vote_generated"), get(vote));
        return response.data;
    } catch (error) {
        console.error("vyskytla sa chyba sendVoteParliament: " + JSON.stringify(error, null, 2) );
        throw error;
    }
}
