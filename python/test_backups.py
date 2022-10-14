"""
Hacked together a script to test the capabilities of backing up and restoring an anvil instance
"""
from web3 import Web3
import requests
import os
from lib import get_droplets, get_contract, send_txn, WALLET_ADDR
import sys


def execute_txns(w3):
    contract = get_contract(w3)
    txn = {
        "from": WALLET_ADDR,
        "maxFeePerGas": w3.toWei(10, 'gwei'),
        "maxPriorityFeePerGas": w3.toWei(1, 'gwei'),
        "nonce": w3.eth.get_transaction_count(WALLET_ADDR),
    }
    tx = contract.functions.setNumber(69).buildTransaction(txn)
    send_txn(w3, tx)


def check_state(w3):
    contract = get_contract(w3)
    number = contract.functions.number().call()
    print(f'Number: {number}')


def check_event(w3):
    contract = get_contract(w3)
    events = contract.events.SetNumber.createFilter(fromBlock=0).get_all_entries()
    print(f'Number of events: {len(events)}')
    print(events)


def dump_state(url):
    requests.post(url)


def reset_state(ip):
    response = requests.post(f"http://{ip}:8545", json={
        "jsonrpc": "2.0",
        "method": "anvil_reset",
        "id": 100
    })
    return response.json()


def load_state(url):
    requests.post(url, json={
        "id": 0
    }, auth=(os.environ["BASIC_AUTH_USER"], os.environ["BASIC_AUTH_PASSWORD"]))


def main(dump_url, load_url):
    droplets = get_droplets()
    for droplet in droplets:
        ip = droplet['attributes']['ipv4_address']
        w3 = Web3(Web3.HTTPProvider(f'http://{ip}:8545'))
        
        # simulate transaction
        # execute_txns(w3)
        # check_state(w3)
        # check_event(w3)
        
        # # call backup
        # dump_state(dump_url)
        
        # reset the chain
        # result = reset_state(ip)
        # print(result)
        # check_state(w3)
        # check_event(w3)
        
        # # restore the chain
        load_state(load_url)
        check_state(w3)
        check_event(w3)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <DUMP_URL> <LOAD_URL>")
        print("Where URLs are DigitalOcean Function URLs")
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2])
