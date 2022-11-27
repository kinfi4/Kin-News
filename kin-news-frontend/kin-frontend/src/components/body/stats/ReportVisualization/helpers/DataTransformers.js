export const transformObjectToArray = (data, xName, yName) => {
    return Object.entries(data).map(el => {
        let obj = {};
        obj[xName] = el[0];
        obj[yName] = el[1];

        return obj;
    });
}
