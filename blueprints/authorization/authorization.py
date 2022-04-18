import datetime
import random
import string
from . import utils
import cryptocode
import flask
import mnemonic
import sqlalchemy.orm
from flask_login import login_user
from db_utils import db_session
from db_models import users
from .forms import authorization, register

blueprint = flask.Blueprint(
    'auth_blueprint',
    __name__,
    template_folder='templates'
)


@blueprint.route('/login/', methods=['GET', 'POST'])
def login_page():
    form = authorization.AuthorizationForm()
    if flask.request.method == 'GET':
        return flask.render_template('login.html', form=form)
    else:
        with db_session.create_session() as session:
            session: sqlalchemy.orm.Session
            user = session.query(users.User).filter(users.User.fingerprint == flask.request.form.get('fp'),
                                                    users.User.secured_code == flask.request.cookies.get(
                                                        'secured_code')).first()
            if user:
                mnemo = mnemonic.Mnemonic('english')
                if mnemo.check(cryptocode.decrypt(user.mnemo, user.fingerprint + form.password.data)):
                    secured_code = utils.generate_secure_code()
                    login_user(user, duration=datetime.timedelta(minutes=30))
                    user.secured_code = secured_code
                    resp = flask.make_response(flask.redirect('/'))
                    resp.set_cookie('secured_code', secured_code, max_age=datetime.timedelta(days=90))
                    session.commit()
                    return resp
            else:
                flask.flash('User is not found')
                resp = flask.make_response(flask.redirect('/registration/'))
                resp.delete_cookie('secured_code')
                return resp


@blueprint.route('/registration/', methods=['GET', 'POST'])
def registration_page():
    form = register.RegisterForm()
    if flask.request.method == 'GET':
        return flask.render_template('registration.html', form=form)
    else:
        if form.validate_on_submit():
            with db_session.create_session() as session:
                session: sqlalchemy.orm.Session
                if form.password.data != form.password_again.data:
                    return flask.render_template('registration.html',
                                                 form=form,
                                                 message="Passwords do not match")
                encode_mnemo = cryptocode.encrypt(form.mnemo.data, flask.request.form.get('fp') + form.password.data)
                mnemo = mnemonic.Mnemonic('english')
                if mnemo.check(form.mnemo.data):
                    secured_code = utils.generate_secure_code()
                    user = users.User(
                        fingerprint=flask.request.form.get('fp'),
                        mnemo=encode_mnemo,
                        secured_code=secured_code
                    )

                    session.add(user)
                    session.commit()
                    login_user(user, duration=datetime.timedelta(minutes=30))

                    resp = flask.make_response(flask.redirect('/'))
                    resp.set_cookie('secured_code', secured_code, max_age=datetime.timedelta(days=90))
                    return resp
                else:
                    return flask.render_template('registration.html',
                                                 form=form,
                                                 message="Incorrect mnemonic phrase")
