from web3 import Web3

RPC = "http://localhost:8545"

w3 = Web3(Web3.HTTPProvider(RPC))

print(w3.isConnected())