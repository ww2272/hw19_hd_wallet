from constants import *
import subprocess
import os
import json
from web3 import Web3
import web3
from eth_account import Account
import bit
from bit.network import NetworkAPI
#from web3.middleware import geth_poa_middleware




mnemonic = os.getenv('MNEMONIC', 'waste orbit flush video wrist smoke cause skull decade merry live myself')
def derive_wallets(mnemonic, coin, numderive):
    command = './derive -g --mnemonic=' + '"' + mnemonic + '"' + ' --coin=' + coin + ' --numderive=' + numderive + ' --format=json'
    #print(command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    accounts = json.loads(output)
    return(accounts)


coins = {'btc-test': derive_wallets(mnemonic, BTCTEST, '3'), 'eth': derive_wallets(mnemonic, ETH, '3')}

def priv_key_to_account(coin, priv_key):
    if coin == 'btc-test':
        return bit.PrivateKeyTestnet(priv_key)
    if coin == 'eth':
        return Account.privateKeyToAccount(priv_key)

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

def create_tx(coin, account, to, amount):
    if coin == 'btc-test':
        return bit.PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])
    if coin == 'eth':
        gasEstimate = w3.eth.estimateGas({"from": account.address, "to": to, "value": amount})
        return {
        "from": account.address,
        "to": to,
        "value": amount,
        "gasPrice": w3.eth.gasPrice,
        "gas": gasEstimate,
        "nonce": w3.eth.getTransactionCount(account.address),
        "chainId": w3.eth.chainId
        }
account_one = priv_key_to_account(BTCTEST, coins[BTCTEST][0]['privkey'])
account_two = priv_key_to_account(ETH,'0x2eb487ca088e1ece1c165918b40cb871601f3369bca2ac249fc0fdbe1bd208d9')
#create_tx(BTCTEST, account_one, 'mjR7fjJDrZJWhue2iK3A2CzPWAkZJqpaaF', 10)
#create_tx(ETH, account_two, '0x17c3fE20737abD3E9722A738533B07c891805Df9', 10)  

def send_tx(coin, account, to, amount):
    raw_tx=create_tx(coin, account, to, amount)
    if coin == 'btc-test':
        signed = account.sign_transaction(raw_tx)
        return NetworkAPI.broadcast_tx_testnet(signed)
    if coin == 'eth':
        signed = account.sign_transaction(raw_tx)
        return w3.eth.sendRawTransaction(signed.rawTransaction)

#send_tx(ETH, account_two, '0x17c3fE20737abD3E9722A738533B07c891805Df9', 10)


