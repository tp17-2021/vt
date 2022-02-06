import axios from "axios";

export async function sendVoteParliament(party: number, candidates: [])
{
    let data = {
        party: party,
        candidates: candidates
    };
    try {
        let response = await axios.post("/backend/api/vote_generated", data);
        return response.data;
    } catch (error) {
        console.log(error);
        alert("vyskytla sa chyba sendVoteParliament: " + JSON.stringify(error, null, 2) );
        return null;
    }
}

export async function getConfig()
{
    let response = await axios.get("/config_files/config.json");
    // let response = await axios.get("/backend/api/election/config");
    return response.data;
}