# anvil-instancing
Dockerizing [anvil from foundry](https://book.getfoundry.sh/anvil/) to run on Digital Ocean Droplets, to act as lightweight private chains

The instance(s) are accessible through typical JSON RPC clients (ethers.js, web3py).

I.e. web clients can submit transactions (free) to the RPC to represent progression or outcomes of a game. Events can be parsed (via the RPC) and used for rendering the outcomes.

---

# Features

* Simplified infrastructure deployment and container initialization via Terraform. No need to click through web interfaces; minimal command-lines

* Host a multitude of anvil instances for scaling

* Automated state-instantiation. Define game logic as a contract, and automatically deploy it to the private chain when anvil instances are created

* Anvil is fast -- it runs on affordable, lightweight machines (1 vCPU / 1GB RAM)

* Flexible -- modify the Dockerfile to add additional parameters to the anvil instance (i.e. block times, gas limit, starting balances, etc)

**Trade Offs**

* Anvil does not support subscriptions [docs](https://book.getfoundry.sh/reference/anvil/)

* To minimize memory and disk consumption, anvil instances should be restarted or reset occasionally. This means the chain's state should be considered *emphemeral*

---

# Configuration
Off-the-shelf modifications to tailor your private anvil node:

1. Modify `src/Counter.sol` and `Counter.s.sol` with any contracts you want to deploy when starting the *private* anvil node
    1. For example: deploy game logic, assets-as-NFTs, etc
3. Find `ANVIL_START` in the `Dockerfile` and attach additional [anvil flags](https://book.getfoundry.sh/reference/anvil/)

# Setup

Requirements & Dependencies:
* Docker installed & configured with Docker Hub. You should be able to push your docket 
* [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli#install-terraform) installed
* Copy `.env.sample` to `.env`
    1. See in-line comments on how to set the values
    2. **Note**: it is recommended to create an SSH key separate from your default github SSH key. This separate SSH key will be used for SSH'ing into the droplets, and can be shared with teammates.

1. Build the Docker Image for Digital Ocean Droplets (take note of `--platform` flag, especially on Apple Silicon machines)

    `docker build --platform linux/amd64 --tag saucepoint/anvil-instancing .`

    (replace the docker repository with your own)

2. Push to Docker Hub

    `docker push saucepoint/anvil-instancing`

    (replace the docker repository with your own)

3. Create & start the Anvil instances (Droplets), via Terraform
    1. `cd terraform`
    2. `source ../.env` -- set variables for Terraform
    3. `terraform init` -- installs the DigitalOcean provider
    4. `terraform apply` -- creates required infrastructure; starts the containers on the newly created droplets

5. Verify that clients can connect to the RPCs. Run the `liveness.py` in `/python` directory