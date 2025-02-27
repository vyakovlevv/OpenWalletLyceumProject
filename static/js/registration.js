let degree_refresh_button = 0

function show_errors(errors) {
    document.querySelector('.errors').innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-x"\n' +
        '                     viewBox="0 0 16 16">\n' +
        '                    <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"></path>\n' +
        '                </svg>' + errors
}

document.querySelector('.refresh-mnemo-button').addEventListener('click', function (e) {
    e.preventDefault()
    degree_refresh_button += 360
    const url = '/api/mnemo/refresh'
    let refresh_icon = document.querySelector('.refresh-icon')
    refresh_icon.style.transform = 'rotate(' + degree_refresh_button + 'deg)'
    refresh_icon.setAttribute('transform', 'rotate(180deg)')
    fetch(url, {'method': 'GET'}).then(async r => {
        const response = await r.json()
        document.querySelector('.mnemo-phrase').value = response['result']
    })
})

document.querySelector('#registration-form').addEventListener('submit', function (e) {
    e.preventDefault()
    // const fp = document.querySelector('#fingerprint').querySelector('input').value
    const fp = "testfp"; // fixme
    const mnemo = document.querySelector('.mnemo-phrase').value
    const password = document.querySelector('#password').value
    const password_again = document.querySelector('#password-again').value
    const url_check_mnemo = '/api/mnemo/check'
    let error = ''
    if (password !== password_again) {
        error = 'Entered passwords do not match'
    }
    if (mnemo === '') {
        error = 'Enter mnemo phrase'
    }
    if (password === '' && password_again === '') {
        error = 'Enter passwords'
    }
    if (error !== '') {
        show_errors(error)
    } else {
        fetch(url_check_mnemo, {
            'method': 'POST',
            'body': JSON.stringify({'mnemo': mnemo})
        }).then(async r => {
            const response = await r.json()
            if (response['status'] === 'ok' && response['result']) {
                const url_registration = '/registration/'
                fetch(url_registration, {
                    'method': 'POST',
                    'body': JSON.stringify({
                        'mnemo': mnemo,
                        'password': password,
                        'fp': fp,
                    })
                }).then(async r => {
                    const response = await r.json()
                    if (response['status'] === 'ok') {
                        window.location.href = response['result']['redirect']
                    } else {
                        show_errors(response['message'])
                    }
                })
            } else {
                if (response['status'] !== 'ok') {
                    show_errors(response['message'])
                } else {
                    show_errors('Incorrect mnemo phrase')
                }
            }
        })
    }
})