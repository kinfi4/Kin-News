import {showMessage} from "./messages";

export function truncate(str, n){
    return (str.length > n) ? str.slice(0, n-1) + '...' : str;
}


export function translateDateToString(date) {
    console.log(date.getMonth() + 1)
    return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`;
}

export function shuffle(array) {
    return array.sort(() => 0.5 - Math.random());
}


export function downloadFile(url, contentType='csv') {
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/' + contentType
        },
    })
        .then((response) => {
            response.blob().then(blob => {
                showMessage([{message: 'Downloading started', type: 'success'}])

                const url = window.URL.createObjectURL(
                    new Blob([blob]),
                );

                const link = document.createElement('a');

                link.href = url;
                link.download = "Report-Data." + contentType;

                document.body.appendChild(link);
                link.click();
                link.parentNode.removeChild(link);
            })
        })
        .catch(err => {
            console.log(err)
            showMessage([{message: "Report exporting failed(", type: 'danger'}])
        });

}