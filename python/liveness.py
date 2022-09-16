from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://157.230.12.179:8545"))

print(w3.isConnected())