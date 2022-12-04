export function truncate(str, n){
    return (str.length > n) ? str.slice(0, n-1) + '...' : str;
}


export function translateDateToString(date) {
    return `${date.getDate()}/${date.getMonth()}/${date.getFullYear()}`;
}

export function shuffle(array) {
    return array.sort(() => 0.5 - Math.random());
}
