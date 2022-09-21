Some simple scripts to verify RPC configuration and availability.

**Assumes that Droplet IP addresses can be read from terraform state file**

# Recommended Setup

```bash
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

python liveness.py
```

# Benchmark Results

Executed with `multitime -n 50` (50 runs). Results measured in seconds

Macbook Pro 16inch - M1 Pro / 16 GB RAM
```
1: python benchmark.py http://127.0.0.1:8545
            Mean        Std.Dev.    Min         Median      Max
real        0.335       0.030       0.286       0.340       0.398       
user        0.279       0.018       0.247       0.282       0.318       
sys         0.041       0.006       0.031       0.042       0.052
```

Digital Ocean Droplet (Docker) - 1 vCPU / 1GB RAM
```
1: python benchmark.py http://159.203.105.5:8545
            Mean        Std.Dev.    Min         Median      Max
real        0.925       0.116       0.797       0.892       1.336       
user        0.339       0.012       0.296       0.341       0.364       
sys         0.044       0.005       0.036       0.044       0.067
```

Desktop PC - i7 8700k / 16 GB RAM
