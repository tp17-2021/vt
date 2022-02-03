// if candidate.name matches searchFilter
export function filterCandidate(candidates, searchFilter) {
    return filter(candidates, searchFilter, "name");
}

function filter(haystack, needle, filterBy) {
    if (haystack === null) {
        return [];
    }
    return [...haystack.filter(candidate => normalize(candidate[filterBy]).includes(normalize(needle)))];
}

function normalize(str) {
    return removeAccents(str.toLowerCase());
}

function removeAccents(str) {
    return str.normalize('NFD').replace(/[\u0300-\u036f]/g, "");
}