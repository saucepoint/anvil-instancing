# anvil-instancing
Dockerizing [anvil from foundry](https://book.getfoundry.sh/anvil/) to run on Digital Ocean Droplets, to act as a lightweight private chain

---

As builders look to enable chain-faciliated games, they arrive at a crossroad -- *what portions of the system should be onchain?.* Some will choose only to have game assets/components represented as NFTs, while game logic resides on traditional web2 backends. Others will go all out with a fully on-chain experience. In the middle, some will a adopt a hybrid approach.

This repo is meant for the hybrid games, where game logic is executed on the EVM through a private chain. This reduces the cost burden of operational systems and/or end-users.

**End Result**

Create a private, configurable, EVM environment that is accessible through typical JSON RPC clients (ethers.js, web3py).

For example, web clients can submit transactions to the RPC to represent progression or outcomes of a game. Events can be parsed (via the RPC) and used for rendering the outcomes.

**Trade Offs**

* Anvil does not support subscriptions [docs](https://book.getfoundry.sh/reference/anvil/)

* To minimize disk consumption, anvil instances should be restarted or reset occasionally. This means the chain's state should be considered *emphemeral*

---

# Features

* Simplified infrastructure deployment via Terraform. No need to click through web interfaces; minimal command-lines

* Host a multitude of anvil instances for scaling

* Automated state-instantiation. Define game logic as a contract, and automatically deploy it to the private chain when anvil instances are created

* Anvil is fast -- it runs on affordable, lightweight machines (1 vCPU / 1GB RAM)

* Flexible -- modify the Dockerfile to add additional parameters to the anvil instance (i.e. block times, gas limit, starting balances, etc)

---


# Setup

Requirements & Dependencies:
* Docker installed & configured with Docker Hub
* Terraform installed

1. Build the Docker Image for Digital Ocean Droplets (take note of `--platform` flag, especially on Apple Silicon machines)

    `docker build --platform linux/amd64 --tag saucepoint/anvil-instancing .`


2. Push to Docker Hub

    `docker push saucepoint/anvil-instancing`

3. Create Droplet with firewall rules, via Terraform
    1. `cd terraform`
    3. `terraform init`
    4. `terraform apply`

4. SSH into Droplet & Start the docker container
    
    `ssh root@<DROPLET IP> "docker pull docker.io/saucepoint/anvil-instancing && docker run -p 8545:8545 -d saucepoint/anvil-instancing`

5. Verify that clients can connect. Run the `liveness.py` in `/python` direcotry