/**
 * Get candidates array for a chosen party
 * @param chosenPartyId
 */
import type {Icandidate} from "../api/stores";
import {get} from "svelte/store";
import {parties} from "../api/stores";

export function findPartyById(chosenPartyId: string): Icandidate[] {
    const party = get(parties).find(party => party._id === chosenPartyId);
    return party ? party : null;
}

export function findCandidatesByPartyId(chosenPartyId: number): Icandidate[] {
    return get(parties).find(party => party._id === chosenPartyId).candidates
}

export function findCandidateById(candidates: Icandidate[], candidateId: number): Icandidate {
    return candidates.find(candidate => candidate._id === candidateId)
}
