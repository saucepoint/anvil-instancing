"""
Basic benchmarking test to compare anvil's speed on Digital Ocean vs
Local machines.

Not really meant for production use, just hacked this together
"""
import sys
from web3 import Web3
import json

def _sendTxn(w3, txn):
    # default foundry wallet, so not a security concern lol
    WALLET_PRIV = 'ac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'
    signed_txn = w3.eth.account.sign_transaction(txn, WALLET_PRIV)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_hash

def benchmark(rpc_address):
    # addresses returned by a default anvil instance
    CONTRACT_ADDR = '0x5FbDB2315678afecb367f032d93F642f64180aa3'
    WALLET_ADDR = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
    
    w3 = Web3(Web3.HTTPProvider(rpc_address))
    
    with open('../out/Counter.sol/Counter.json') as f:
        contract_json = json.load(f)
        abi = contract_json['abi']
    contract = w3.eth.contract(address=CONTRACT_ADDR, abi=abi)

    txn = {
        "from": WALLET_ADDR,
        "maxFeePerGas": w3.toWei(10, 'gwei'),
        "maxPriorityFeePerGas": w3.toWei(1, 'gwei'),
    }

    # ----------------- Benchmarking -----------------
    # 1. Call Counter.increment()
    # 2. Call Counter.incrementMany(128)
    # 3. Call Counter.setNumber(69)
    # 4. Read Counter.number()
    
    txn['nonce'] = w3.eth.get_transaction_count(WALLET_ADDR)
    tx = contract.functions.increment().buildTransaction(txn)
    _sendTxn(w3, tx)

    txn['nonce'] = w3.eth.get_transaction_count("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266")
    tx = contract.functions.incrementMany(128).buildTransaction(txn)
    _sendTxn(w3, tx)

    txn['nonce'] = w3.eth.get_transaction_count("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266")
    tx = contract.functions.setNumber(69).buildTransaction(txn)
    _sendTxn(w3, tx)

    contract.functions.number().call()


# Should really use argparse, but this is just a quick solution
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <RPC>")
    print("\tThe RPC should have src/Counter.sol deployed")
    sys.exit(1)
else:
    benchmark(sys.argv[1])