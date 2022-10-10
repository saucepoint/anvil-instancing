"""
Basic benchmarking test to compare anvil's speed on Digital Ocean vs
Local machines.

Not really meant for production use, just hacked this together
"""
import sys
from web3 import Web3
from lib import get_contract, WALLET_ADDR, send_txn


def benchmark(rpc_address):
    w3 = Web3(Web3.HTTPProvider(rpc_address))
    
    contract = get_contract(w3)

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
    send_txn(w3, tx)

    txn['nonce'] = w3.eth.get_transaction_count("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266")
    tx = contract.functions.incrementMany(128).buildTransaction(txn)
    send_txn(w3, tx)

    txn['nonce'] = w3.eth.get_transaction_count("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266")
    tx = contract.functions.setNumber(69).buildTransaction(txn)
    send_txn(w3, tx)

    contract.functions.number().call()


if __name__ == '__main__':
    # Should really use argparse, but this is just a quick solution
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <RPC>")
        print("\tThe RPC should have src/Counter.sol deployed")
        sys.exit(1)
    else:
        benchmark(sys.argv[1])
