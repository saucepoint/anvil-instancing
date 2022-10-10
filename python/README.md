# Contents:

* [Persistence](#persistence) - back up & restore anvil state

* [Liveness](#liveness) - verify connectivity of the RPC

* [Benchmarks](#benchmark-results) - Performance benchmarks across different DigitalOcean Droplets. (TLDR: equal performance even on the smallest instance)

# Persistence

Anvil state is *emphemeral* and is deleted when the process is killed. However, state can be saved and restored via [anvil_dumpState and anvil_loadState](https://book.getfoundry.sh/reference/anvil/)

These RPC calls are scheduled and invoked via serverless functions in `anvil-state/`. These dirt-cheap serverless functions are powered by [DigitalOcean's Functions](https://www.digitalocean.com/products/functions).

## Get Started:

Unfortunately DigitalOcean Functions are not deployable with Terraform *yet*. We'll need to run some commands to get setup:

[Additional DigitalOcean Documentation](https://docs.digitalocean.com/products/functions/quickstart/)

1. Have [`doctl` CLI](https://docs.digitalocean.com/reference/doctl/how-to/install/) installed and configured

2. `doctl serverless install` - installs the `doctl serverless` sub-CLI commands

3. `doctl serverless connect` - connect to the DigitalOcean Functions service

3. `doctl serverless namespaces create --label anvil-state --region nyc1` - creates a Namespace, which organizes a collection of functions

3. `doctl serverless deploy anvil-state` - deploy our serverless functions!

## Dumping State
* `anvil/dump` is scheduled to run every 5 minutes, defined [here](anvil-state/packages/project.yml)

* files are saved based to [object storage](#object-storage)

## Restoring State
* `anvil/load` will allow you to restore state from one of your backups
* Arguments:
    * `id` - the index/number associated with the RPC defined in [.env](anvil-state/.env.sample)
    * `backup_path` - an optional path to specify which backup file to use. Formatted as `backups/anvil{i}/state-{timestamp}.txt`
        * Omitting `backup_path` will restore the state from the default `latest/anvil{i}.txt`
* via API:
    * `curl -H "Content-Type: application/json" -X POST --data '{"id":0}' <function-url>`
* via CLI:
    * `doctl serverless functions invoke anvil/load -p id:0`


## Object Storage

Anvil-state (hex string) is saved to DigitalOcean Spaces (S3-clone). Assuming the base Terraform was applied, the buckets and expiration policy should be already configured.

* The state is saved to 2 locations:
    * `anvil-state-XXXXXXXX/backups/anvil{i}/state-{timestamp}.txt` - everytime a backup is called, a new file is created here. However Terraform has configured the `backups/` directory to only hold the objects for **5 days**
    * `anvil-state-XXXXXXXX/latest/anvil{i}.txt` - the most recently backed-up state. Does not expire, but is overwritten on each backup

---

# Liveness

Verify the availability of the RPC

**Assumes that Droplet IP addresses can be read from terraform state file**

```bash
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

python liveness.py
```

---

# Benchmark Results

Executed `benchmark.py`, which simulates a few contract calls, with `multitime -n 50` (50 runs).

### TLDR: Anvil performs equally across different Droplet sizes
Therefore, the 1 vCPU / 1GB RAM is the recommended instance. (1 vCPU / 512 MB is unavailable for Docker-included Droplets).


If you want to circumvent Docker and run anvil *directly* on a 1 vCPU / 512 MB, checkout [example terraform](../terraform/1vcpu-512mb.example)

> The latency compared to a local anvil instance is most likely due to accessing the RPC over a network

![Benchmark Chart](https://pbs.twimg.com/media/FdNkL-2XEAAI9Vf?format=png&name=900x900)

Results measured in seconds:

### M1 Pro / 16 GB RAM - Macbook Pro 16inch
```
    1: python benchmark.py http://127.0.0.1:8545
                Mean        Std.Dev.    Min         Median      Max
    real        0.335       0.030       0.286       0.340       0.398       
    user        0.279       0.018       0.247       0.282       0.318       
    sys         0.041       0.006       0.031       0.042       0.052
```

### 1 vCPU / 512 MB RAM - Digital Ocean Droplet (Native)

(Runs anvil directly, without Docker)
```
    1: python benchmark.py http://68.183.119.180:8545
                Mean        Std.Dev.    Min         Median      Max
    real        1.003       0.170       0.783       0.953       1.472       
    user        0.355       0.039       0.286       0.355       0.440       
    sys         0.049       0.007       0.036       0.049       0.066
```

### 1 vCPU / 1GB RAM - Digital Ocean Droplet (Docker)

```
    1: python benchmark.py http://159.203.105.5:8545
                Mean        Std.Dev.    Min         Median      Max
    real        0.925       0.116       0.797       0.892       1.336       
    user        0.339       0.012       0.296       0.341       0.364       
    sys         0.044       0.005       0.036       0.044       0.067
```

### 1 vCPU / 1GB RAM - Digital Ocean Droplet (Native) 

(Runs anvil directly, without Docker)
```
    1: python benchmark.py http://165.22.33.184:8545
                Mean        Std.Dev.    Min         Median      Max
    real        0.872       0.041       0.788       0.869       1.003       
    user        0.321       0.017       0.281       0.324       0.350       
    sys         0.042       0.005       0.035       0.042       0.062
```


### AMD 1 vCPU / 1GB RAM - Digital Ocean Droplet (Native)

```
    1: python benchmark.py http://157.230.62.76:8545
                Mean        Std.Dev.    Min         Median      Max
    real        0.950       0.160       0.766       0.898       1.641       
    user        0.335       0.025       0.290       0.333       0.408       
    sys         0.044       0.007       0.034       0.043       0.069
```

### Intel 1 vCPU / 1GB RAM - Digital Ocean Droplet (Native)

```
    1: python benchmark.py http://157.230.49.29:8545
                Mean        Std.Dev.    Min         Median      Max
    real        0.963       0.177       0.807       0.883       1.716       
    user        0.338       0.014       0.314       0.337       0.370       
    sys         0.041       0.005       0.034       0.041       0.067
```

### 1 vCPU / 2GB RAM - Digital Ocean Droplet (Native)

```
                Mean        Std.Dev.    Min         Median      Max
    real        1.042       0.215       0.813       0.959       1.638       
    user        0.357       0.033       0.288       0.355       0.418       
    sys         0.048       0.007       0.036       0.046       0.062
```

### AMD 1 vCPU / 2GB RAM - Digital Ocean Droplet (Native)

```
    1: python benchmark.py http://157.230.0.65:8545
                Mean        Std.Dev.    Min         Median      Max
    real        1.048       0.273       0.828       0.933       2.036       
    user        0.329       0.028       0.275       0.325       0.412       
    sys         0.042       0.006       0.034       0.040       0.066 
```

### Intel 1 vCPU / 2GB RAM - Digital Ocean Droplet (Native)

```
    1: python benchmark.py http://157.230.49.254:8545
                Mean        Std.Dev.    Min         Median      Max
    real        1.095       0.240       0.876       0.997       2.049       
    user        0.387       0.027       0.295       0.392       0.435       
    sys         0.048       0.007       0.035       0.049       0.064
```

### 2 vCPU / 2GB RAM - Digital Ocean Droplet (Native)

```
    1: python benchmark.py http://157.230.62.10:8545
                Mean        Std.Dev.    Min         Median      Max
    real        1.136       0.332       0.818       0.984       2.262       
    user        0.367       0.037       0.292       0.360       0.437       
    sys         0.048       0.008       0.035       0.048       0.067       
```

### AMD 2 vCPU / 2GB RAM - Digital Ocean Droplet (Native)

```
    1: python benchmark.py http://157.230.62.202:8545
                Mean        Std.Dev.    Min         Median      Max
    real        1.000       0.209       0.807       0.915       1.759       
    user        0.331       0.020       0.274       0.335       0.383       
    sys         0.041       0.005       0.034       0.041       0.065 
```

### Intel 2 vCPU / 2GB RAM - Digital Ocean Droplet (Native)

```
    1: python benchmark.py http://157.230.53.229:8545
                Mean        Std.Dev.    Min         Median      Max
    real        1.027       0.255       0.781       0.915       1.940       
    user        0.336       0.029       0.286       0.335       0.408       
    sys         0.043       0.006       0.034       0.043       0.062
```
