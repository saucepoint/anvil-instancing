# anvil-instancing
Dockerizing anvil to run on digital ocean, to act as a lightweight private chain.

---

As builders look to enable chain-faciliated games, they arrive at a crossroad -- *what portions of the system should be onchain?.* Some will choose only to have game assets/components represented as NFTs, while game logic resides on traditional web2 backends. Others will go all out with a fully on-chain experience. In the middle, some will a adopt a hybrid approach.

This repo is meant for the hybrid games, where game logic is executed on the EVM through a private chain. This reduces the cost burden of operational systems and/or end-users.


# Setup

1. Build Docker Image for Digital Ocean Droplets (take note of `--platform linux/amd64` flag, especially on Apple Silicon machines)

    `docker build --platform linux/amd64 -t saucepoint/anvil-instancing . --no-cache`


2. Push to Docker Hub

    `docker push saucepoint/anvil-instancing`

3. Create Droplet

4. SSH into Droplet

5. Start the anvil