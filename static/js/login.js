function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function show_errors(errors) {
    document.querySelector('.errors').innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-x"\n' +
        '                     viewBox="0 0 16 16">\n' +
        '                    <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"></path>\n' +
        '                </svg>' + errors
}

document.querySelector('#login-form').addEventListener('submit', function (e) {
    e.preventDefault()
    const url = '/login/'
    // const fp = document.querySelector('#fingerprint').querySelector('input').value
    const fp = "testfp"; // FIXME
    const password = document.querySelector('#password').value
    fetch(url, {
        'method': 'POST',
        'body': JSON.stringify({
            'fp': fp,
            'password': password,
            'secured_code': getCookie('secured_code')
        })
    }).then(async r => {
        const response = await r.json()
        if (response['status'] === 'ok') {
            window.location.href = response['result']['redirect']
        } else {
            show_errors(response['message'])
        }
    })
})