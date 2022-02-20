import axios from "axios";

export async function sendVoteParliament(party: number, candidates: [])
{
    let data = {
        party_id: party,
        candidate_ids: candidates
    };
    try {
        let response = await axios.post("/backend/api/vote_generated", data);
        return response.data;
    } catch (error) {
        console.error("vyskytla sa chyba sendVoteParliament: " + JSON.stringify(error, null, 2) );
        return null;
    }
}

export async function getConfig()
{
    try {
        let response = await axios.get("/config_files/config.json");
        // let response = await axios.post("/backend/api/election/config");
        return response.data;
    } catch (error) {
        console.error("vyskytla sa chyba getConfig: " + JSON.stringify(error, null, 2) );
        return null;
    }
}