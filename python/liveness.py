from web3 import Web3
import json

# Read the droplets' IP addresses from the terraform state file
with open('../terraform/terraform.tfstate') as f:
    tfstate = json.load(f)
    droplet_resource = list(filter(lambda x: x['type'] == 'digitalocean_droplet', tfstate.get('resources', [])))[0]
    droplets = droplet_resource.get('instances', [])

# Attempt to connect to each anvil node hosted on each droplet
for droplet in droplets:
    ip = droplet['attributes']['ipv4_address']
    rpc_url = f'http://{ip}:8545'
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    print(ip, f'Successful Connection: {w3.isConnected()}')
