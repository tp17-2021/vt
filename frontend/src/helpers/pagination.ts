export function paginate(filtered, page, perPage) {
    const start = (page - 1) * perPage;
    const end = start + perPage;
    return filtered.slice(start, end);
}