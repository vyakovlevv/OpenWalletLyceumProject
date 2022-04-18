import flask
from flask_login import login_required, current_user

blueprint = flask.Blueprint(
    'home_blueprint',
    __name__,
    template_folder='templates'
)


@blueprint.route('/home')
@login_required
def homepage():
    return 'home'
