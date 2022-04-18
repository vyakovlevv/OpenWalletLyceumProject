import os
import flask_login
from db_utils import db_session
from blueprints.authorization import authorization
from blueprints.home import home
from flask import Flask, request, render_template, redirect
import bfa
from db_models.users import User
from flask_restful import Api
from flask_login import LoginManager, login_required, logout_user, current_user
from config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index_map():
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
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/database.db")
    app.register_blueprint(authorization.blueprint)
    app.register_blueprint(home.blueprint)
    # api.add_resource(user_resource.UsersListResource, '/api/users')
    app.run(port=os.getenv('PORT', 8080), host='0.0.0.0')
