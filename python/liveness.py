from web3 import Web3
from lib import get_droplets

def main():
    droplets = get_droplets()
    # Attempt to connect to each anvil node hosted on each droplet
    for droplet in droplets:
        ip = droplet['attributes']['ipv4_address']
        rpc_url = f'http://{ip}:8545'
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        print(ip, f'Connected: {w3.isConnected()}')


if __name__ == '__main__':
    main()