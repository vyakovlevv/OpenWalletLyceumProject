import base64
import string

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
        r = requests.post(f"{flask.request.host_url}/api/users/tokens", data=data, cookies=cookies)
        print(r.json())
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
