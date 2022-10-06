"""
Script for backing up the Anvil state to Digital Ocean Spaces
  * copied into the Docker container
  * scheduled as a cron job to run every 5 minutes (configured in Dockerfile)
"""
import requests
import boto3
import datetime


def backup():
    """Backup the Anvil state to Digital Ocean Spaces"""
    
    # fetch the state from the Anvil RPC
    response = requests.post("0.0.0.0:8545", data={
        "jsonrpc": "2.0",
        "method": "anvil_dumpState",
        "params": [],
        "id": 1
    })
    state_hex = response.json()["result"]

    # configure the Digital Ocean Spaces client
    session = boto3.session.Session()
    client = session.client(
        "s3",
        region_name="nyc3",
        endpoint_url="https://nyc3.digitaloceanspaces.com",
        aws_access_key_id="DO_SPACES_KEY",
        aws_secret_access_key="DO_SPACES_SECRET"
    )

    # save to backups (expire after 5 days)
    client.put_object(
        Bucket="anvil_state",
        Key=f"backups/state-{datetime.datetime.utcnow().isoformat()}.txt",
        Body=state_hex
    )

    # save to latest (overwrite / does not expire)
    client.put_object(
        Bucket="anvil_state",
        Key="latest.txt",
        Body=state_hex
    )

if __name__ == "__main__":
    backup()