FROM ubuntu:20.04

SHELL ["/bin/bash", "-c"]

RUN apt update

RUN apt install -y curl git

# install foundry
RUN curl -L https://foundry.paradigm.xyz | bash

RUN /root/.foundry/bin/foundryup

# run the node
CMD /root/.foundry/bin/anvil --chain-id 8118 --host 0.0.0.0
