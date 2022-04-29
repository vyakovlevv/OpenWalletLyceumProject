import base64
import json
import string

import mnemonic
from . import utils
from config import SECRET_KEY
import cryptocode
import flask
import qrcode
import os
import random

import requests
from flask_login import login_required, current_user

blueprint = flask.Blueprint(
    'home_blueprint',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@blueprint.route('/home', methods=['GET', 'POST'])
@login_required
def homepage():
    if flask.request.method == 'GET':
        return flask.render_template('home.html')
    else:
        data = {
            'abbreviation': flask.request.form.get('abbreviation'),
            'full_name': flask.request.form.get('full_name'),
            'blockchain': flask.request.form.get('blockchain').split('_')[0],
            'blockchain_gecko_id': flask.request.form.get('blockchain').split('_')[1],
            'contract_address': flask.request.form.get('contract_address')
        }
        cookies = {}
        for key, val in flask.request.cookies.items():
            cookies[key] = val
        domen = '/'.join(flask.request.base_url.split('/')[:3])
        print(f'HOST URL: {domen}')
        r = requests.post(f"{domen}api/users/tokens", data=data, cookies=cookies)
        print(f"HOST REQUEST:{r.url}")
        print(f"HTTP STATUS CODE: {r.status_code}")
        return flask.redirect('/')


@blueprint.route('/api/qr')
def api_qr_addresses():
    address = flask.request.args.get('address')
    if address:
        img = qrcode.make(address)
        name = f'{"".join(random.choices(string.ascii_letters, k=8))}.jpg'
        img.save(name)
        with open(name, 'rb') as f:
            encoded_string = b'data:image/png;base64, ' + base64.b64encode(f.read())
        os.remove(name)
        return {'status': 'ok', 'result': encoded_string.decode('utf-8')}
    return {'status': 'error', 'message': 'Bad request'}


@blueprint.route('/api/transaction/checkPassword', methods=['POST'])
def api_transaction_check_password():
    data = json.loads(flask.request.data)
    if data.get('password'):
        mnemo = mnemonic.Mnemonic('english')
        if mnemo.check(cryptocode.decrypt(current_user.mnemo, current_user.fingerprint + data.get('password'))):
            return {'status': 'ok'}
        return {'status': 'error', 'message': 'incorrect password'}
    return {'status': 'error', 'message': 'Missing password'}


@blueprint.route('/api/transaction', methods=['POST'])
def api_transaction():
    data = json.loads(flask.request.data)
    mnemo_class = mnemonic.Mnemonic('english')
    mnemo = cryptocode.decrypt(current_user.mnemo, current_user.fingerprint + data.get('password'))
    blockchain_gecko_id = data.get('blockchain_gecko_id')
    if mnemo_class.check(mnemo):
        if blockchain_gecko_id == 'binance-smart-chain':
            r = utils.withdrawal_tokens_in_ethereum_similar_networks('https://rpc.ankr.com/bsc',
                                                                     data.get('destination_address'),
                                                                     data.get('amount_tokens'), mnemo,
                                                                     data.get('contract_address'), 56)
            return r
        elif blockchain_gecko_id == 'ethereum':
            r = utils.withdrawal_tokens_in_ethereum_similar_networks('https://rpc.ankr.com/eth',
                                                                     data.get('destination_address'),
                                                                     data.get('amount_tokens'), mnemo,
                                                                     data.get('contract_address'), 1)
            return r

    return {'status': 'error', 'message': 'Authentication error'}
