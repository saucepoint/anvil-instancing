"""
A simple shared source of functions & constants for the python scripts
"""
from web3 import Web3
import json


# default foundry wallet, so not a security concern lol
WALLET_PRIV = 'ac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'

# addresses returned by a default anvil instance
CONTRACT_ADDR = '0x5FbDB2315678afecb367f032d93F642f64180aa3'
WALLET_ADDR = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'


def send_txn(w3, txn):
    signed_txn = w3.eth.account.sign_transaction(txn, WALLET_PRIV)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_hash


def get_contract(w3):
    with open('../out/Counter.sol/Counter.json') as f:
        contract_json = json.load(f)
        abi = contract_json['abi']
    contract = w3.eth.contract(address=CONTRACT_ADDR, abi=abi)
    return contract


def get_droplets():
    # Read the droplets' IP addresses from the terraform state file
    with open('../terraform/terraform.tfstate') as f:
        tfstate = json.load(f)
        droplet_resource = list(filter(lambda x: x['type'] == 'digitalocean_droplet', tfstate.get('resources', [])))[0]
        droplets = droplet_resource.get('instances', [])
    return droplets
