import axios from "axios";
import {configLoaded, parties, texts, vote} from "./stores";
import {get} from "svelte/store";


export async function loadConfig()
{
    try {
        let response = await axios.get("/config_files/config.json");
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
        let response = await axios.post("/backend/api/vote_generated", get(vote));
        return response.data;
    } catch (error) {
        console.error("vyskytla sa chyba sendVoteParliament: " + JSON.stringify(error, null, 2) );
        throw error;
    }
}
