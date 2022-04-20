import flask
from db_utils.db_session import create_session
from db_models.tokens import Token
from db_models.users import User
from flask_restful import reqparse, abort, Resource

parser = reqparse.RequestParser()
parser.add_argument('abbreviation', required=True)
parser.add_argument('full_name', required=True)
parser.add_argument('blockchain', required=True)
parser.add_argument('contract_address', required=False)


class TokensListResource(Resource):
    """API Endpoint for add tokens"""

    def post(self):
        """Add tokens"""
        session = create_session()
        args = parser.parse_args()
        if session.query(Token).filter(Token.abbreviation == args['abbreviation'],
                                       Token.blockchain == args['blockchain']).first():
            return flask.jsonify({'status': 'error', 'message': 'Abbreviation in this blockchain already exists'})
        if session.query(Token).filter(Token.contract_address == args['contract_address'],
                                       Token.blockchain == args['blockchain']).first():
            return flask.jsonify({'status': 'error', 'message': 'Contract address in this blockchain already exists'})
        token = Token(
            abbreviation=args['abbreviation'],
            full_name=args['full_name'],
            blockchain=args['blockchain'],
            contract_address=args['contract_address'] if args['contract_address'] else None  # Fixme сделать .pyi файл
        )
        session.add(token)
        session.commit()
        return flask.jsonify({'status': 'OK'})


class UserTokenListResource(Resource):
    def get(self):
        required_args = ['offset', 'indexStart', 'fp', 'secured_code']
        for arg in required_args:
            if arg not in flask.request.args:
                return flask.jsonify({'status': 'error', 'message': f'Missing an argument: {arg}'})
        session = create_session()
        user = session.query(User).filter(User.fingerprint == flask.request.args.get('fp'),
                                          User.secured_code == flask.request.args.get('secured_code')).first()
        if user:
            data = user.tokens[int(flask.request.args.get('indexStart')):int(flask.request.args.get('indexStart')) + 15]
            return {'status': 'ok',
                    'tokens': [i.to_dict(only=('abbreviation', 'full_name', 'blockchain', 'current_price')) for i in
                               data]}
        return flask.jsonify({'status': 'error', 'message': 'User not found'})
