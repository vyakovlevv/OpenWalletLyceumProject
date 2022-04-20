function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}


function loader_data() {
    const url = '/api/users/tokens';
    const data = {
        offset: 15,
        indexStart: 0,
        fp: document.querySelector('#fingerprint').querySelector('input').value,
        secured_code: getCookie('secured_code')
    }
    const readyURI = url + '?offset=' + data.offset + '&indexStart=' + data.indexStart + '&fp=' + data.fp + '&secured_code=' + data.secured_code
    const response = fetch(readyURI, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const json = response.json();
    alert(json)
}

document.addEventListener('DOMContentLoaded', loader_data, false);