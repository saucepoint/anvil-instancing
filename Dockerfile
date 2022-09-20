FROM ubuntu:20.04

SHELL ["/bin/bash", "-c"]

RUN apt update

RUN apt install -y curl git

# install foundry
RUN curl -L https://foundry.paradigm.xyz | bash

RUN /root/.foundry/bin/foundryup

# recreate the foundry directory structure inside the container
RUN mkdir /root/lib
RUN mkdir /root/script
RUN mkdir /root/src

# copy the contracts to the container
COPY lib/ /root/lib
COPY script/ /root/script
COPY src/ /root/src
COPY .gitmodules /root/
COPY foundry.toml /root/

# need to set the directory so `forge script` can do relative imports
WORKDIR /root

# Runs `forge script` against the anvil chain to set up contracts
ENV INIT_SCRIPTS='/root/.foundry/bin/forge script /root/script/Counter.s.sol --chain-id 8118 --rpc-url http://0.0.0.0:8545 --private-key ac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80  --silent --broadcast'

# Command to start the anvil service
# Add your flags commands here
ENV ANVIL_START='/root/.foundry/bin/anvil --chain-id 8118 --host 0.0.0.0'

# Execute the scripts after the anvil service is started
CMD (sleep 5 && $INIT_SCRIPTS) & $ANVIL_START