import cryptocode
import flask
import mnemonic
import requests
from db_utils.db_session import create_session
from db_models.tokens import Token
from db_models.users_tokens import UsersToken
from flask_login import current_user
from db_models.users import User
from config import SECRET_KEY
from . import utils
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
        exist_token = session.query(Token).filter(Token.abbreviation == flask.request.form['abbreviation'],
                                                  Token.blockchain == flask.request.form['blockchain']).first()
        if exist_token:
            return flask.jsonify({'status': 'ok', 'result': exist_token.id})
        exist_token = session.query(Token).filter(Token.contract_address == flask.request.form['contract_address'],
                                                  Token.blockchain == flask.request.form['blockchain']).first()
        if exist_token:
            return flask.jsonify({'status': 'ok', 'result': exist_token.id})
        token = Token(
            abbreviation=flask.request.form['abbreviation'],
            full_name=flask.request.form['full_name'],
            blockchain=flask.request.form['blockchain'],
            blockchain_gecko_id=flask.request.form.get('blockchain_gecko_id'),
            contract_address=flask.request.form['contract_address'] if flask.request.form['contract_address'] else None,
            color=utils.generate_unique_hex_color()
        )
        session.add(token)
        session.commit()
        print(f"TOKEN ID: {token.id}")
        return flask.jsonify({'status': 'ok', 'result': token.id})


class UserTokenListResource(Resource):
    def get(self):
        try:
            required_args = ['offset', 'indexStart', 'fp', 'secured_code']
            verdict = utils.control_required_keys(flask.request.args, required_args)
            if verdict != 'ok':
                return flask.jsonify({'status': 'error', 'message': f'Missing an argument: {verdict}'})
            session = create_session()
            user = session.query(User).filter(User.fingerprint == flask.request.args.get('fp'),
                                              User.secured_code == flask.request.args.get('secured_code')).first()
            if user:
                data = user.tokens[
                       int(flask.request.args.get('indexStart')):int(flask.request.args.get('indexStart')) + 15]
                tokens = []
                for i in data:
                    try:
                        token = i.token.to_dict(only=('abbreviation', 'full_name', 'blockchain', 'current_price', 'color'))
                        params = {
                            'token': i.token.abbreviation,
                            'fp': flask.request.args.get('fp'),
                            'blockchain_gecko_id': i.token.blockchain_gecko_id if i.token.blockchain_gecko_id else '',
                            'token_address': i.token.contract_address if i.token.contract_address else ''
                        }
                        cookies = {}
                        for key, val in flask.request.cookies.items():
                            cookies[key] = val
                        domen = '/'.join(flask.request.base_url.split('/')[:3])
                        r = requests.get(f"{domen}/api/user/token", params=params, cookies=cookies).json()
                        if r['status'] == 'ok':
                            token['address'] = r['result']['address']
                            token['balance'] = r['result']['balance']
                            tokens.append(token)
                    except Exception as ex:
                        print(ex)
                return {'status': 'ok',
                        'tokens': tokens}
            return flask.jsonify({'status': 'error', 'message': 'User not found'})
        except Exception as ex:
            print(ex)
            return {'status': 'error', 'message': 'Unexpected error'}

    def post(self):
        try:
            session = create_session()
            data = {
                'abbreviation': flask.request.form.get('abbreviation'),
                'full_name': flask.request.form.get('full_name'),
                'blockchain': flask.request.form.get('blockchain'),
                'blockchain_gecko_id': flask.request.form.get('blockchain_gecko_id'),
                'contract_address': flask.request.form.get('contract_address')
            }
            r = requests.post(f"{flask.request.host_url}/api/tokens", data=data).json()
            users_token = UsersToken(
                user_id=current_user.id,
                token_id=r['result']
            )
            session.add(users_token)
            session.commit()
            return {'status': 'ok'}
        except Exception as ex:
            print(ex)
            return {'status': 'error', 'message': 'Unexpected error'}


class UserTokenResource(Resource):
    def get(self):  # получить адрес и баланс
        required_args = ['token', 'fp', 'blockchain_gecko_id', 'token_address']
        verdict = utils.control_required_keys(flask.request.args, required_args)
        if verdict != 'ok':
            return flask.jsonify({'status': 'error', 'message': f'Missing an argument: {verdict}'})
        session = create_session()
        user = session.query(User).filter(User.fingerprint == flask.request.args.get('fp'),
                                          User.secured_code == flask.request.cookies.get('secured_code')).first()
        if user:
            mnemo = cryptocode.decrypt(user.mnemo, flask.request.args.get('fp') + cryptocode.decrypt(
                flask.request.cookies.get('__p'), SECRET_KEY))
            if mnemonic.Mnemonic('english').check(mnemo):
                address = None
                balance = None
                token = flask.request.args.get('token')
                blockchain_gecko_id = flask.request.args.get('blockchain_gecko_id')
                if token == 'BTC' and not blockchain_gecko_id:
                    address = utils.get_address_btc(mnemo)
                    r = requests.get(f'https://blockchain.info/q/addressbalance/{address}')
                    balance = int(r.text) / 100000000
                elif token == 'BNB' and blockchain_gecko_id == 'binance-smart-chain':
                    address = utils.get_address_eth(mnemo)
                    balance = utils.get_balance_ethereum_similar_coins('https://rpc.ankr.com/bsc', address)
                elif token == 'ETH' and blockchain_gecko_id == 'ethereum':
                    address = utils.get_address_eth(mnemo)
                    balance = utils.get_balance_ethereum_similar_coins('https://rpc.ankr.com/eth', address)
                else:
                    if blockchain_gecko_id == 'binance-smart-chain':
                        address = utils.get_address_eth(mnemo)
                        balance = utils.get_balance_ethereum_similar_tokens('https://rpc.ankr.com/bsc', address,
                                                                            flask.request.args.get('token_address'))
                    elif blockchain_gecko_id == 'ethereum':
                        address = utils.get_address_eth(mnemo)
                        balance = utils.get_balance_ethereum_similar_tokens('https://rpc.ankr.com/eth', address,
                                                                            flask.request.args.get('token_address'))
                return {'status': 'ok', 'result': {
                    'address': address,
                    'balance': balance
                }}
            else:
                return {'status': 'error', 'message': 'Authentication error'}

        else:
            return {'status': 'error', 'message': 'User not found'}
