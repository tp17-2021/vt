export interface IpaginationObject {
    items: any[];
    paginatedItems: any[];
    searchTerm: string;
    currentPageNumber: number;
    countOfPages: number;
    itemsPerPage: number;
    searchBy: string[];
}

export function paginate(filtered, page, perPage) {
    const start = (page - 1) * perPage;
    const end = start + perPage;
    return filtered.slice(start, end);
}

export function getNumberOfPages(filtered, perPage) {
    return Math.ceil(filtered.length / perPage);
}

function search(objectsToFilter, searchTerm: string, searchBy: string[]) {
    if (searchTerm === '') {
        return objectsToFilter;
    }
    return objectsToFilter.filter(object => {
        return searchBy.some(key => {
            let filterProperty = object[key];
            // if filterProperty is number, convert to string
            if (typeof filterProperty === "number") {
                filterProperty = filterProperty.toString();
            }
            return normalize(filterProperty).includes(normalize(searchTerm));
        });
    });
}

function normalize(str) {
    return removeAccents(str.toLowerCase());
}

function removeAccents(str) {
    return str.normalize('NFD').replace(/[\u0300-\u036f]/g, "");
}

export function searchAndPaginate(paginationObject: IpaginationObject): void {
    const filtered = search(paginationObject.items, paginationObject.searchTerm, paginationObject.searchBy);
    paginationObject.countOfPages = getNumberOfPages(filtered, paginationObject.itemsPerPage);
    paginationObject.paginatedItems = paginate(filtered, paginationObject.currentPageNumber, paginationObject.itemsPerPage);
}