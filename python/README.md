Some simple scripts to verify RPC configuration and availability.

**Assumes that Droplet IP addresses can be read from terraform state file**

# Recommended Setup

```bash
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

python liveness.py
```