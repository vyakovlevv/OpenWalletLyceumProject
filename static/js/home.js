function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}


let data = {
    labels: [
        'Red',
        'Blue',
        'Yellow'
    ],
    datasets: [{
        label: 'Statistics your crypto portfolio',
        data: [],
        backgroundColor: [],
        hoverOffset: 4
    }]
};

const config = {
    type: 'doughnut',
    data: data,
    options: {
        plugins: {
            legend: {
                display: false
            }
        },
        'borderAlign': 'inner',
        'radius': 150,
    },

};

let myChart = null

// const timerFetchTokensId = setInterval(, 3000);
function send_funds(item_data) {
    let modal_window = document.querySelector('#modal-window-send-funds')
    document.querySelector('#blockchain_gecko_id-input-form').value = item_data['blockchain_gecko_id']
    document.querySelector('#contract_address-input-form').value = item_data['contract_address']
    modal_window.style.display = 'block'
}

function receive_funds(address) {
    let modal_window = document.querySelector('#modal-window-receive-funds')
    modal_window.style.display = 'block'
    document.querySelector('.text-modal-window-receive-funds').innerHTML = 'Your address:\n' + address
    const url = '/api/qr?address=' + address
    fetch(url, {'method': 'GET'}).then(async r => {
        const json = await r.json();
        document.querySelector('.expand-data-modal-window-receive-funds').innerHTML = '<img src="' + json['result'] + '"/>'
    })
}

function try_show_chart_statistics() {
    if (data['datasets'][0]['data'].length > 0) {
        myChart = new Chart(
            document.getElementById('statistics_crypto_chart'),
            config
        );
        document.querySelector('.content-home').style.marginTop = -800 + 'px'
    }
}

function addTokenElement(item_data, parent) {
    let button = document.createElement('button')
    button.className = 'collapsible'
    button.style.backgroundColor = item_data['color']
    button.innerHTML = '<div class="text-full-name-collapse-content">' + item_data['full_name'] + '</div>' +
        '<div class="text-blockchain-collapse-content">(' + item_data['blockchain'] + ')</div>' +
        '<div class="text-amount-collapse-content">' + item_data['balance'] + '</div>'
    parent.append(button)
    if (item_data['balance'] > 0 && item_data['current_price'] > 0) {
        data['datasets'][0]['data'].push(item_data['current_price'] * item_data['balance'])
        data['datasets'][0]['backgroundColor'].push(item_data['color'])
    }

    let div = document.createElement('div')
    div.className = 'item-collapse-content'
    parent.append(div)
    div.innerHTML = '<button class="MuiButtonBase-root MuiButton-root MuiButton-outlined MuiButton-outlinedPrimary button-receive-funds"\n' +
        '                            tabindex="0" type="button"><span class="MuiButton-label"><span\n' +
        '                            class="MuiButton-startIcon MuiButton-iconSizeMedium"><svg\n' +
        '                            class="MuiSvgIcon-root" focusable="false" viewBox="0 0 24 24"\n' +
        '                            aria-hidden="true"><path fill-rule="evenodd"\n' +
        '                                                     d="M14 6V4h-4v2h4zM4 8v11h16V8H4zm16-2c1.11 0 2 .89 2 2v11c0 1.11-.89 2-2 2H4c-1.11 0-2-.89-2-2l.01-11c0-1.11.88-2 1.99-2h4V4c0-1.11.89-2 2-2h4c1.11 0 2 .89 2 2v2h4z"></path></svg></span>Receive</span><span\n' +
        '                            class="MuiTouchRipple-root"></span></button>\n' +
        '                    <button class="MuiButtonBase-root MuiButton-root MuiButton-outlined MuiButton-outlinedPrimary button-send-funds"\n' +
        '                            tabindex="0" type="button"><span class="MuiButton-label"><span\n' +
        '                            class="MuiButton-startIcon MuiButton-iconSizeMedium"><svg\n' +
        '                            class="MuiSvgIcon-root" focusable="false" viewBox="0 0 24 24"\n' +
        '                            aria-hidden="true"><path\n' +
        '                            d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"></path></svg></span>Send</span><span\n' +
        '                            class="MuiTouchRipple-root"></span></button>' +
        '<div>Your address:</div>' +
        '<div class="text-address-collapse-content">' + item_data['address'] + '</div>'
    let modal_window_receive_funds = document.querySelector('#modal-window-receive-funds')
    div.querySelector('.button-receive-funds').addEventListener('click', function (e) {
        receive_funds(item_data['address'])
    })
    document.querySelector('.close-modal-window-receive-funds').addEventListener('click', function (e) {
        modal_window_receive_funds.style.display = "none";
    })
    window.addEventListener('click', function (e) {
        if (e.target == modal_window_receive_funds) {
            modal_window_receive_funds.style.display = "none";
        }
    })
    let modal_window_send_funds = document.querySelector('#modal-window-send-funds')
    div.querySelector('.button-send-funds').addEventListener('click', function (e) {
        send_funds(item_data)
    })
    document.querySelector('.close-modal-window-send-funds').addEventListener('click', function (e) {
        modal_window_send_funds.style.display = "none";
    })
    window.addEventListener('click', function (e) {
        if (e.target == modal_window_send_funds) {
            modal_window_send_funds.style.display = "none";
        }
    })
    button.addEventListener('click', function () {
        this.classList.toggle('active')
        let next_div = this.nextElementSibling
        if (next_div.style.maxHeight) {
            next_div.style.maxHeight = null
        } else {
            next_div.style.maxHeight = next_div.scrollHeight + 'px'
        }
    })

}

function load_tokens() {
    const data_request = {
        offset: 15,
        indexStart: 0,
        // fp: document.querySelector('#fingerprint').querySelector('input').value,
        fp: "testfp", // FIXME
        secured_code: getCookie('secured_code')
    }
    const content_home = document.querySelector('.content-token-home')
    const url = '/api/users/tokens' + '?offset=' + data_request.offset + '&indexStart=' + data_request.indexStart + '&fp=' + data_request.fp + '&secured_code=' + data_request.secured_code
    fetch(url, {'method': 'GET'}).then(async r => {
        const json = await r.json();
        if (json['status'] === 'ok') {
            for (let i = 0; i < json['tokens'].length; i++) {
                addTokenElement(json['tokens'][i], content_home)
            }
            try_show_chart_statistics()
        } else {
            alert(json['message'])
        }
    })
}

document.addEventListener('DOMContentLoaded', function () {
    setTimeout(load_tokens, 500)
}, false);
let modal_window_add_token = document.querySelector('#modal-window-add-token')
document.querySelector('.add-token-button').addEventListener('click', function () {
    modal_window_add_token.style.display = 'block'
})


document.querySelector('.close-modal-window-add-token').addEventListener('click', function (e) {
    modal_window_add_token.style.display = "none";
})
window.addEventListener('click', function (e) {
    if (e.target == modal_window_add_token) {
        modal_window_add_token.style.display = "none";
    }
})

document.querySelector('#form-modal-send-funds').addEventListener('submit', function (e) {
    e.preventDefault()
    let errors_container = document.querySelector('#errors-modal-send-funds')
    const blockchain_gecko_id = document.querySelector('#blockchain_gecko_id-input-form').value
    const contract_address = document.querySelector('#contract_address-input-form').value
    const destination_address = document.querySelector('#destination_address-modal-window').value
    const amount_tokens = document.querySelector('#amount-modal-window').value
    const password = document.querySelector('#wallet_password-modal-window').value
    const url_check_password = '/api/transaction/checkPassword'
    fetch(url_check_password, {
        'method': 'POST',
        'body': JSON.stringify({'password': password})
    }).then(async r => {
        const json = await r.json();
        if (json['status'] === 'ok') {
            const url_transaction = '/api/transaction'
            fetch(url_transaction, {
                'method': 'POST',
                'body': JSON.stringify({
                    'password': password,
                    'blockchain_gecko_id': blockchain_gecko_id,
                    'contract_address': contract_address,
                    'destination_address': destination_address,
                    'amount_tokens': amount_tokens
                })}).then(async r => {
                const json = await r.json();
                if (json['status'] === 'ok') {
                    alert('Transaction completed successfully\nTx hash: ' + json['result'])
                } else {
                    errors_container.innerHTML = json['message']
                }
            })
        } else {
            errors_container.innerHTML = json['message']
        }
    })
})