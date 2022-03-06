import {writable} from "svelte/store";


export enum ElectionTypes {
    PARLIAMENT = "parliament",
}

export const electionType = writable(ElectionTypes.PARLIAMENT);


/**
 example:
 {
    "_id": 0,
    "party_number": 1,
    "order": 1,
    "first_name": "Jozef",
    "last_name": "Sásik",
    "degrees_before": "Ing.",
    "age": 61,
    "occupation": "predseda SĽS Andreja Hlinku",
    "residence": "Banská Bystrica"
},
 */


export interface Icandidate {
    _id: number;
    party_number: number;
    order: number;
    first_name: string;
    last_name: string;
    degrees_before: string;
    age: number;
    occupation: string;
    residence: string;
}

/**
 example:
 {
    "_id": 0,
    "party_number": 1,
    "name": "Slovenská ľudová strana Andreja Hlinku",
    "abbreviation": "Slovenská ľudová strana (SĽS)",
    "image": "slovenska-ludova-strana-andreja-hlinku.png",
    "image_bytes": "iVBORw0KGg... ...CYII=",
    "candidates": []
}
 */
export interface Iparty {
    _id: number;
    party_number: number;
    name: string;
    abbreviation: string;
    image: string;
    image_bytes: string;
    candidates: Icandidate[];
}

export interface Itexts {
    elections_name_short: {
        en: string,
        sk: string
    },
    elections_name_long: {
        en: string,
        sk: string
    },
    elections_date: {
        en: string,
        sk: string
    }
}

// example: config files/config.json
export interface Iconfig {
    polling_places: [],
    parties: Iparty[],
    key_pairs: [],
    texts: Itexts
}

export const configLoaded = writable(false);
export const parties = writable([]);
export const texts = writable([]);


export const vote = writable({
    party_id: null,
    candidates_ids: []
});