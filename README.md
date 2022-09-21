# anvil-instancing
Dockerizing [anvil from foundry](https://book.getfoundry.sh/anvil/) to run on Digital Ocean Droplets, to act as lightweight private chains

The instance(s) are accessible through typical JSON RPC clients (ethers.js, web3py).

i.e. web clients can submit free transactions to the RPC to represent progression or outcomes of a game. Events can be parsed (via the RPC) and used for rendering the outcomes.

---

# Features

* Simplified infrastructure deployment and container initialization via Terraform. No need to click through web interfaces; minimal command-lines

* Host a multitude of anvil instances for scaling

* Automated state-instantiation. Define game logic as a contract, and automatically deploy it to the private chain when anvil instances are created

* Anvil is fast -- it runs on affordable, lightweight instances (1 vCPU / 1GB RAM) - [Benchmarks](python/README.md#benchmark-results)

* Flexible -- modify the Dockerfile to add additional parameters to the anvil instance (i.e. block times, gas limit, starting balances, etc)

**Trade Offs**

* To minimize memory and disk consumption, anvil instances should be restarted or reset occasionally. This means the chain's state should be considered *emphemeral*

---

# Configuration
Off-the-shelf modifications to tailor your private anvil node:

1. Modify/Replace [src/Counter.sol](src/Counter.sol) and [script/Counter.s.sol](script/Counter.s.sol) with any contracts you want to deploy when starting the *private* anvil node
    1. For example: deploy game logic, assets-as-NFTs, etc
3. Find `ANVIL_START` in the [Dockerfile](Dockerfile) and attach additional [anvil flags](https://book.getfoundry.sh/reference/anvil/)

# Setup

Requirements & Dependencies:
* Docker installed & [configured with Docker Hub](https://docs.docker.com/docker-hub/#step-3-download-and-install-docker-desktop). You should be able to push your docker container to the Hub
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

    > If you are using a new SSH key, you may need to add it to your agent:
    >
    > eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_NEW_SSH_KEY_NON_PUB

5. Verify that clients can connect to the RPCs. Run the `liveness.py` in `/python` directory

## Destroying
Great for starting over or shutting down your prototype

To destroy the instances, firewall, and SSH key:
```
cd terraform
terraform destroy
```
