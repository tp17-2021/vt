import axios from "axios";

export async function sendVoteParliament(party: number, candidates: [])
{
    let data = {
        party: party,
        candidates: candidates
    };
    let response = await axios.post("/backend/api/vote_generated", data);
    return response.data;
}