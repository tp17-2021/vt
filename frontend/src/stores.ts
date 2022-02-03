import {get, writable} from 'svelte/store';
import {navigateTo} from "svelte-router-spa";
import {set} from "svelte-router-spa/types/store";


interface dataInterface {
    title: string;
    type: string;
    subtitle: string;
    parties: Array<{
        _id: string;
        party_number: number;
        name: string;
        abbreviation: string;
        image: string;
        candidates: Array<{
            _id: string;
            party_number: number;
            order: string;
            first_name: string;
            last_name: number;
            degrees_before: string;
            age: number;
            occupation: string;
            residence: string;
            party_id: string;
        }>;
    }>;
}

// interface dataInterfaceOld {
//     title: string;
//     subtitle: string;
//     parties: any[];
//     candidates: Array<{
//         id: number;
//         img: string;
//         name: string;
//         degree: string;
//         age: number;
//         profession: string;
//         city: string;
//     }>;
// }

let data = {} as dataInterface;
export const configIsLoading = writable(true);
export const config = writable({});

export const tokenValid = writable(false);
export const chosenParty = writable(null);
export const chosenCandidates = writable([]);

// if debug is true in localStorage
export const debugEnabled = writable(localStorage.getItem("debug") === "true");
window.debug = function (flag: boolean) {
    localStorage.setItem("debug", flag.toString());
    location.reload();
};



let homeRoute : string = '/';
// listen on page load
window.addEventListener('load', () => {
    (async () => {
        // api call simulation, will query gateway in the future
        data = await fetch("/config_files/config.json").then(x => x.json())

        // temporarily permanent json format converter
        data.parties.forEach(party => {
            party.id = party.party_number;
            party.img = party.image;
            party.candidates.forEach(candidate => {
                // if (candidate.hasOwnProperty("party_number")) {
                candidate.id = candidate.order;
                candidate.name = candidate.first_name + " " + candidate.last_name;
                candidate.degree = candidate.degrees_before;
                candidate.profession = candidate.occupation;
                candidate.city = candidate.residence;
                // }
            })
        })


        config.set(data);
        configIsLoading.set(false);

        if (data.type === "parliament") {
            homeRoute = "/parliament/scan";
        } else {
            homeRoute = "/presidential/scan";
        }

        setTimeout(() => {
            tokenValid.subscribe(tokenValidValue => {
                console.log("TOKEN changed", tokenValidValue)

                if (!tokenValidValue) {
                    resetVote();
                }
            })
        }, 1000)
    })()
});

export function resetVote() {
    if (get(tokenValid)) {
        console.log("reset vote to false in resetVote")
        tokenValid.set(false);
    }
    navigateTo(homeRoute);
    setTimeout(() => {
        chosenParty.set(null);
        chosenCandidates.set([]);
    }, 1000)
}