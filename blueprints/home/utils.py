import random
import string
from py_crypto_hd_wallet import HdWalletBip44Coins, HdWalletBipWordsNum, HdWalletBipLanguages, HdWalletBipFactory, \
    HdWalletBipChanges
from web3 import Web3


def generate_unique_hex_color():
    """
    return: color in hex format
    """
    return '#' + ''.join(random.choices(string.digits + string.ascii_lowercase[:6], k=6))


def control_required_keys(data: dict, required_keys: list) -> str:
    """Function to check for entry of the required keys in data"""
    for key in required_keys:
        if key not in data:
            return key
    return 'ok'


def get_hd_wallet(mnemo: str, coin):
    hd_wallet_fact = HdWalletBipFactory(coin)
    hd_wallet = hd_wallet_fact.CreateFromMnemonic("my_wallet_nam", mnemo)
    hd_wallet.Generate(addr_num=1)
    return hd_wallet


def get_address_btc(mnemo, coin=HdWalletBip44Coins.BITCOIN):
    hd_wallet = get_hd_wallet(mnemo, coin)
    return hd_wallet.ToDict()['address']['address_0']['address']


def get_address_eth(mnemo):
    return get_address_btc(mnemo, HdWalletBip44Coins.ETHEREUM)


def get_balance_ethereum_similar_coins(uri_node: str, address: str) -> float:
    w3 = Web3(Web3.HTTPProvider(uri_node))
    balance = w3.fromWei(w3.eth.get_balance(address), 'ether')
    return float(balance)


def get_balance_ethereum_similar_tokens(uri_node: str, wallet_address: str, token_address: str):
    w3 = Web3(Web3.HTTPProvider(uri_node))
    abi = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"assetProtectionRole","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"betaDelegateWhitelister","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"proposedOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"EIP712_DOMAIN_HASH","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"supplyController","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"currentOwner","type":"address"},{"indexed":true,"name":"proposedOwner","type":"address"}],"name":"OwnershipTransferProposed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"oldProposedOwner","type":"address"}],"name":"OwnershipTransferDisregarded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"oldOwner","type":"address"},{"indexed":true,"name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"addr","type":"address"}],"name":"AddressFrozen","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"addr","type":"address"}],"name":"AddressUnfrozen","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"addr","type":"address"}],"name":"FrozenAddressWiped","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"oldAssetProtectionRole","type":"address"},{"indexed":true,"name":"newAssetProtectionRole","type":"address"}],"name":"AssetProtectionRoleSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"SupplyIncreased","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"SupplyDecreased","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"oldSupplyController","type":"address"},{"indexed":true,"name":"newSupplyController","type":"address"}],"name":"SupplyControllerSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"},{"indexed":false,"name":"seq","type":"uint256"},{"indexed":false,"name":"fee","type":"uint256"}],"name":"BetaDelegatedTransfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"oldWhitelister","type":"address"},{"indexed":true,"name":"newWhitelister","type":"address"}],"name":"BetaDelegateWhitelisterSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"newDelegate","type":"address"}],"name":"BetaDelegateWhitelisted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"oldDelegate","type":"address"}],"name":"BetaDelegateUnwhitelisted","type":"event"},{"constant":false,"inputs":[],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"initializeDomainSeparator","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_addr","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_proposedOwner","type":"address"}],"name":"proposeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"disregardProposeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"claimOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"reclaimBUSD","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_newAssetProtectionRole","type":"address"}],"name":"setAssetProtectionRole","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_addr","type":"address"}],"name":"freeze","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_addr","type":"address"}],"name":"unfreeze","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_addr","type":"address"}],"name":"wipeFrozenAddress","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_addr","type":"address"}],"name":"isFrozen","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_newSupplyController","type":"address"}],"name":"setSupplyController","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_value","type":"uint256"}],"name":"increaseSupply","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_value","type":"uint256"}],"name":"decreaseSupply","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"target","type":"address"}],"name":"nextSeqOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"sig","type":"bytes"},{"name":"to","type":"address"},{"name":"value","type":"uint256"},{"name":"fee","type":"uint256"},{"name":"seq","type":"uint256"},{"name":"deadline","type":"uint256"}],"name":"betaDelegatedTransfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"r","type":"bytes32[]"},{"name":"s","type":"bytes32[]"},{"name":"v","type":"uint8[]"},{"name":"to","type":"address[]"},{"name":"value","type":"uint256[]"},{"name":"fee","type":"uint256[]"},{"name":"seq","type":"uint256[]"},{"name":"deadline","type":"uint256[]"}],"name":"betaDelegatedTransferBatch","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_addr","type":"address"}],"name":"isWhitelistedBetaDelegate","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_newWhitelister","type":"address"}],"name":"setBetaDelegateWhitelister","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_addr","type":"address"}],"name":"whitelistBetaDelegate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_addr","type":"address"}],"name":"unwhitelistBetaDelegate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
    token_address = Web3.toChecksumAddress(token_address)
    token = w3.eth.contract(address=token_address, abi=abi)
    token_balance = token.functions.balanceOf(wallet_address).call()
    return float(w3.fromWei(token_balance, 'ether'))


def withdrawal_tokens_in_ethereum_similar_networks(uri_node, destination_address, amount_tokens, mnemo,
                                                   contract_address, network_id) -> dict:
    """
    Withdrawal of tokens in ethereum-like networks
    :param uri_node: uri where locate node
    :param destination_address: where to send wallet
    :param amount_tokens: amount tokens
    :param mnemo: mnemo phrase of wallet
    :param contract_address: address of contract in ethereum-like blockhain
    :param network_id: blockchain id
    :return: json with status transaction
    """
    try:
        w3 = Web3(Web3.HTTPProvider(uri_node))
        hd_wallet = get_hd_wallet(mnemo, HdWalletBip44Coins.ETHEREUM)
        wallet_address = get_address_eth(mnemo)
        contract_address = w3.toChecksumAddress(contract_address)
        destination_address = w3.toChecksumAddress(destination_address)
        abi = '[{"anonymous": false,"inputs": [{"indexed": true,"internalType": "address","name": "owner",' \
              '"type": "address"},{"indexed": true,"internalType": "address","name": "spender","type": "address"},' \
              '{"indexed": false,"internalType": "uint256","name": "value","type": "uint256"}],"name": "Approval",' \
              '"type": "event"},{"anonymous": false,"inputs": [{"indexed": true,"internalType": "address",' \
              '"name": "from","type": "address"},{"indexed": true,"internalType": "address","name": "to",' \
              '"type": "address"},{"indexed": false,"internalType": "uint256","name": "value","type": "uint256"}],' \
              '"name": "Transfer","type": "event"},{"constant": true,"inputs": [{"internalType": "address",' \
              '"name": "_owner","type": "address"},{"internalType": "address","name": "spender","type": "address"}],' \
              '"name": "allowance","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"payable": ' \
              'false,"stateMutability": "view","type": "function"},{"constant": false,"inputs": [{"internalType": ' \
              '"address","name": "spender","type": "address"},{"internalType": "uint256","name": "amount",' \
              '"type": "uint256"}],"name": "approve","outputs": [{"internalType": "bool","name": "","type": "bool"}],' \
              '"payable": false,"stateMutability": "nonpayable","type": "function"},{"constant": true,"inputs": [{' \
              '"internalType": "address","name": "account","type": "address"}],"name": "balanceOf","outputs": [{' \
              '"internalType": "uint256","name": "","type": "uint256"}],"payable": false,"stateMutability": "view",' \
              '"type": "function"},{"constant": true,"inputs": [],"name": "decimals","outputs": [{"internalType": ' \
              '"uint256","name": "","type": "uint256"}],"payable": false,"stateMutability": "view",' \
              '"type": "function"},{"constant": true,"inputs": [],"name": "getOwner","outputs": [{"internalType": ' \
              '"address","name": "","type": "address"}],"payable": false,"stateMutability": "view",' \
              '"type": "function"},{"constant": true,"inputs": [],"name": "name","outputs": [{"internalType": ' \
              '"string","name": "","type": "string"}],"payable": false,"stateMutability": "view","type": "function"},' \
              '{"constant": true,"inputs": [],"name": "symbol","outputs": [{"internalType": "string","name": "",' \
              '"type": "string"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": true,' \
              '"inputs": [],"name": "totalSupply","outputs": [{"internalType": "uint256","name": "",' \
              '"type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": false,' \
              '"inputs": [{"internalType": "address","name": "recipient","type": "address"},{"internalType": ' \
              '"uint256","name": "amount","type": "uint256"}],"name": "transfer","outputs": [{"internalType": "bool",' \
              '"name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function"},' \
              '{"constant": false,"inputs": [{"internalType": "address","name": "sender","type": "address"},' \
              '{"internalType": "address","name": "recipient","type": "address"},{"internalType": "uint256",' \
              '"name": "amount","type": "uint256"}],"name": "transferFrom","outputs": [{"internalType": "bool",' \
              '"name":"","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function"}] '
        token = w3.eth.contract(address=contract_address, abi=abi)
        token_balance = token.functions.balanceOf(wallet_address).call()
        gas_limit = 80000
        nonce = w3.eth.getTransactionCount(wallet_address)
        if float(float(w3.fromWei(token_balance, 'ether'))) >= float(amount_tokens):
            if w3.eth.get_balance(wallet_address) - (5000000000 * gas_limit) > 0:
                transaction = token.functions.transfer(destination_address,
                                                       int(Web3.toHex(w3.toWei(amount_tokens, 'ether')),
                                                           16)).buildTransaction(
                    {'chainId': network_id,
                     'gas': gas_limit,
                     'gasPrice': w3.toWei(5, 'gwei'),
                     'nonce': nonce})
                signed_tx = w3.eth.account.sign_transaction(transaction,
                                                            hd_wallet.ToDict()['address']['address_0']['raw_priv'])
                tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
                return {'status': 'ok', 'result': str(w3.toHex(tx_hash))}
            return {'status': 'error', 'message': 'Insufficient funds (gas)'}
        return {'status': 'error', 'message': 'Insufficient funds (tokens)'}
    except Exception as ex:
        print(ex)
        return {'status': 'error', 'message': 'Unexpected error'}
