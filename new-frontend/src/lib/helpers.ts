
import type {Icandidate} from "../api/stores";
import {get} from "svelte/store";
import {parties} from "../api/stores";

/**
 * Get candidates array for a chosen party
 * @param chosenPartyId
 */
export function findPartyById(chosenPartyId: string): Icandidate[] {
    const party = get(parties).find(party => party._id === chosenPartyId);
    return party ? party : null;
}

/**
 * Get all candidates (array) for a chosen party id
 * @param chosenPartyId
 */
export function findCandidatesByPartyId(chosenPartyId: number): Icandidate[] {
    return get(parties).find(party => party._id === chosenPartyId).candidates
}

/**
 * Find candidate from an array of candidates
 * @param candidates
 * @param candidateId
 */
export function findCandidateById(candidates: Icandidate[], candidateId: number): Icandidate {
    return candidates.find(candidate => candidate._id === candidateId)
}

/**
 * Base path from environment variable
 */
// @ts-ignore
export const base: string = (import.meta.env.VITE_BASE_PATH ?? "");
console.log("base", base);

/**
 * Is "npm run dev" used to run the app?
 */
export const isDevelopmentMode: boolean = process.env.NODE_ENV === "development"