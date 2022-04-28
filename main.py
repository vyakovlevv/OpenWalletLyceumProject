import os
import flask
from db_utils import db_session
from blueprints.authorization import authorization
from blueprints.home import home
from flask import Flask, request, redirect, make_response
import bfa
from blueprints.home import home_api
from db_models.users import User
import logging
from flask_restful import Api
from flask_login import LoginManager, login_required, logout_user, current_user
from config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


@app.route('/')
def index_map():
    print(flask.request.base_url)
    print(flask.request.url_root)
    print(flask.request.cookies.items())
    if current_user.is_authenticated:
        return redirect('/home')
    elif request.cookies.get('secured_code'):
        return redirect('/login/')
    else:
        return redirect('/registration/')


@app.context_processor
def bfa_flask():
    return bfa.templatetags.bfa.fingerprint_input()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
def logout():
    logout_user()
    resp = make_response(redirect("/"))
    resp.delete_cookie('secured_code')
    resp.delete_cookie('session')
    return resp


@app.route('/block')
@login_required
def block_wallet():
    logout_user()
    resp = make_response(redirect("/"))
    resp.delete_cookie('session')
    return resp


db_session.global_init("db/database.db")
app.register_blueprint(authorization.blueprint)
app.register_blueprint(home.blueprint)
api.add_resource(home_api.TokensListResource, '/api/tokens')
api.add_resource(home_api.UserTokenListResource, '/api/users/tokens')
api.add_resource(home_api.UserTokenResource, '/api/user/token')


if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 8080), host='0.0.0.0')
