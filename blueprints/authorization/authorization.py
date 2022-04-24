import datetime
import json
from . import utils
import cryptocode
import flask
import mnemonic
import sqlalchemy.orm
from flask_login import login_user
from db_utils import db_session
from db_models import users

blueprint = flask.Blueprint(
    'auth_blueprint',
    __name__,
    template_folder='templates'
)


@blueprint.route('/login/', methods=['GET', 'POST'])
def login_page():
    if flask.request.method == 'GET':
        return flask.render_template('login.html', title='Login', now_login=True)
    else:
        try:
            with db_session.create_session() as session:
                session: sqlalchemy.orm.Session
                data = json.loads(flask.request.data)
                control_keys_verdict = utils.control_required_keys(data, ['fp', 'secured_code', 'password'])
                if control_keys_verdict == 'ok':
                    user = session.query(users.User).filter(users.User.fingerprint == data['fp'],
                                                            users.User.secured_code == data['secured_code']).first()
                    if user:
                        mnemo = mnemonic.Mnemonic('english')
                        if mnemo.check(str(cryptocode.decrypt(user.mnemo, user.fingerprint + data['password']))):
                            secured_code = utils.generate_secure_code()
                            login_user(user, duration=datetime.timedelta(minutes=30))
                            user.secured_code = secured_code
                            resp = flask.make_response(flask.jsonify({'status': 'ok', 'result': {
                                'redirect': '/'
                            }}))
                            resp.set_cookie('secured_code', secured_code, max_age=datetime.timedelta(days=90))
                            session.commit()
                            return resp
                        return {'status': 'error', 'message': 'Incorrect password'}
                    else:
                        resp = flask.make_response(flask.jsonify({'status': 'error', 'message': 'User is not found'}))
                        resp.delete_cookie('secured_code')
                        return resp
                return {"status": 'error', 'message': f'Missing an argument: {control_keys_verdict}'}
        except Exception as ex:
            print(ex)
            return {'status': 'error', 'message': 'Unexpected error'}


@blueprint.route('/registration/', methods=['GET', 'POST'])
def registration_page():
    if flask.request.method == 'GET':
        return flask.render_template('registration.html', title='Registration')
    else:
        with db_session.create_session() as session:
            try:
                session: sqlalchemy.orm.Session
                data = json.loads(flask.request.data)
                control_keys_verdict = utils.control_required_keys(data, ['fp', 'mnemo', 'password'])
                if control_keys_verdict == 'ok':
                    encode_mnemo = cryptocode.encrypt(data['mnemo'], data['fp'] + data['password'])
                    mnemo = mnemonic.Mnemonic('english')
                    if mnemo.check(data['mnemo']):
                        secured_code = utils.generate_secure_code()
                        user = users.User(
                            fingerprint=data['fp'],
                            mnemo=encode_mnemo,
                            secured_code=secured_code
                        )

                        session.add(user)
                        session.commit()
                        login_user(user, duration=datetime.timedelta(minutes=30))
                        resp = flask.make_response(flask.jsonify({'status': 'ok', 'result': {
                            'redirect': '/',  # where to redirect
                        }}))
                        resp.set_cookie('secured_code', secured_code, max_age=datetime.timedelta(days=90))
                        return resp
                    else:
                        return {'status': 'error', 'message': 'Incorrect mnemonic phrase'}
                else:
                    return {"status": 'error', 'message': f'Missing an argument: {control_keys_verdict}'}
            except Exception as ex:
                print(ex)
                return {'status': 'error', 'message': 'Unexpected error'}


@blueprint.route('/api/mnemo/refresh')
def refresh_mnemo_api():
    try:
        mnemo = mnemonic.Mnemonic('english')
        return {"status": 'ok', 'result': mnemo.generate(256)}
    except Exception as ex:
        print(ex)
    return {'status': 'error', 'message': 'Unexpected error'}


@blueprint.route('/api/mnemo/check', methods=['POST'])
def check_mnemo_api():
    try:
        mnemo = mnemonic.Mnemonic('english')
        data = json.loads(str(flask.request.data.decode('utf-8')))
        return {"status": 'ok', 'result': mnemo.check(data['mnemo'])}
    except Exception as ex:
        print(ex)
    return {'status': 'error', 'message': 'Unexpected error'}
