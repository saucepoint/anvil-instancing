terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

# Variables will be read in from the environment
# i.e. TF_VAR_do_token (from running `source ../.env`)
variable "do_token" {
  type = string
}

variable "do_ssh_path" {
  type = string
}

# Number of anvil instances (droplets) to create
variable "num_instances" {
  type = number
}

variable "docker_repository" {
  type = string
}


locals {
  dropletNames = {for i in range(var.num_instances): i => "anvil-${i}"}
}

# locals {
#   sizes = [
#     "s-1vcpu-1gb-amd", "s-1vcpu-1gb-intel", "s-1vcpu-2gb", "s-1vcpu-2gb-amd", "s-1vcpu-2gb-intel", "s-2vcpu-2gb", "s-2vcpu-2gb-amd", "s-2vcpu-2gb-intel"
#   ]
# }
locals {
  asizes = [
    "s-1vcpu-1gb-amd", "s-1vcpu-1gb-intel", "s-1vcpu-2gb", "s-1vcpu-2gb-amd", "s-1vcpu-2gb-intel", "s-2vcpu-2gb", "s-2vcpu-2gb-amd", "s-2vcpu-2gb-intel"
  ]
  sizes = {
    for i in range(length(local.asizes)): i => local.asizes[i]
  }
}

# Configure the DigitalOcean Provider
provider "digitalocean" {
  token = var.do_token
}

# SSH key for accessing droplets
resource "digitalocean_ssh_key" "default" {
  name       = "Terraform"
  public_key = file(var.do_ssh_path)
}

# Create a new Anvil Droplet in the nyc3 region
# feel free to copy & paste this to create additional instances
# resource "digitalocean_droplet" "anvil" {
#   for_each = local.dropletNames

#   image  = "docker-20-04"  # Ubuntu 20.04 w/ Docker
#   name   = each.value
#   region = "nyc3"
#   size   = "s-1vcpu-1gb"  # 1 CPU, 1 GB RAM, 25 GB SSD is the minimum spec for the docker image
#   ssh_keys = [digitalocean_ssh_key.default.fingerprint]
#   depends_on = [
#     digitalocean_ssh_key.default
#   ]

#   # Upon creation of the Droplet, SSH into it and run the docker container
#   connection {
#     type        = "ssh"
#     user        = "root"
#     host        = self.ipv4_address
#   }

#   # pull the docker container and start it
#   provisioner "remote-exec" {
#     inline = [
#       "docker pull docker.io/${var.docker_repository}",
#       "docker run -p 8545:8545 -d ${var.docker_repository}"
#     ]
#   }
# }

# Create a new Anvil Droplet in the nyc3 region
# feel free to copy & paste this to create additional instances
resource "digitalocean_droplet" "anvil" {
  for_each = local.sizes
  image  = "ubuntu-22-04-x64"  # Ubuntu 22.04
  name   = "testOptimization-${each.value}"
  region = "nyc1"
  # size   = "s-1vcpu-1gb"  # 1 CPU, 1 GB RAM, 25 GB SSD is the minimum spec for the docker image
  size   = each.value
  ssh_keys = [digitalocean_ssh_key.default.fingerprint]
  depends_on = [
    digitalocean_ssh_key.default
  ]
}

resource "null_resource" "initAnvil" {
  for_each = digitalocean_droplet.anvil
  connection {
    type        = "ssh"
    user        = "root"
    host        = each.value.ipv4_address
  }

  provisioner "remote-exec" {
    inline = [
      "apt install -y curl git",
      "curl -L https://foundry.paradigm.xyz | bash",
      "/root/.foundry/bin/foundryup",
      "mkdir /root/contracts"
    ]
  }

  provisioner "file" {
    source = "../lib"
    destination = "/root/contracts"
  }
  provisioner "file" {
    source = "../script"
    destination = "/root/contracts"
  }
  provisioner "file" {
    source = "../src"
    destination = "/root/contracts"
  }
  provisioner "file" {
    source = "../.gitmodules"
    destination = "/root/contracts/.gitmodules"
  }
  provisioner "file" {
    source = "../foundry.toml"
    destination = "/root/contracts/foundry.toml"
  }


  depends_on = [
    digitalocean_droplet.anvil,
    digitalocean_firewall.anvil8545
  ]
}

resource "null_resource" "startAnvil" {
  for_each = digitalocean_droplet.anvil
  connection {
    type        = "ssh"
    user        = "root"
    host        = each.value.ipv4_address
  }

  provisioner "remote-exec" {
    inline = [
      "nohup /root/.foundry/bin/anvil --chain-id 8118 --host 0.0.0.0 >/dev/null 2>&1 &",
      "sleep 5 && cd /root/contracts && /root/.foundry/bin/forge script /root/contracts/script/Counter.s.sol --chain-id 8118 --rpc-url http://0.0.0.0:8545 --private-key ac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80  --silent --broadcast"
    ]
  }

  depends_on = [
    digitalocean_droplet.anvil,
    digitalocean_firewall.anvil8545,
    null_resource.initAnvil
  ]
}

# Firewall rules, allow for SSH (22) and Anvil RPC (8545)
resource "digitalocean_firewall" "anvil8545" {
  name = "Anvil8545"

  droplet_ids = [for d in digitalocean_droplet.anvil : d.id]

  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "8545"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "1-65535"  # all ports
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "1-65535"  # all ports
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  depends_on = [
    digitalocean_droplet.anvil
  ]
}

# prints out the IP addresses of the droplets
output "anvil_ipv4" {
  value = [for d in digitalocean_droplet.anvil : d.ipv4_address]
}
