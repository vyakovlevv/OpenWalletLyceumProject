import base64
import string

import flask
import qrcode
import os
import random
from flask_login import login_required, current_user

blueprint = flask.Blueprint(
    'home_blueprint',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@blueprint.route('/home')
@login_required
def homepage():
    return flask.render_template('home.html')


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
