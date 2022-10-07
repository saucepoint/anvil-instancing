import os
import requests
import boto3
import datetime


def backup(id, rpc, s3_client):
    # fetch the state from the Anvil RPC
    response = requests.post(f"http://{rpc}", json={
        "jsonrpc": "2.0",
        "method": "anvil_dumpState",
        "params": [],
        "id": 1
    })
    state_hex = response.json()["result"]

    # save to backups (expire after 5 days)
    s3_client.put_object(
        Bucket=os.environ['SPACES_BUCKET_NAME'],
        Key=f"backups/anvil{id}/state-{datetime.datetime.utcnow().isoformat()}.txt",
        Body=state_hex
    )

    # save to latest (overwrite / does not expire)
    s3_client.put_object(
        Bucket=os.environ['SPACES_BUCKET_NAME'],
        Key=f"latest/anvil{id}.txt",
        Body=state_hex
    )


def main(args):
    # configure the Digital Ocean Spaces client
    session = boto3.session.Session()
    client = session.client(
        "s3",
        region_name="nyc3",
        endpoint_url="https://nyc3.digitaloceanspaces.com",
        aws_access_key_id=os.environ["SPACES_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["SPACES_SECRET_ACCESS_KEY"]
    )

    RPCS = os.environ.get('RPCS', '').split(',')
    for i, rpc in enumerate(RPCS):
        backup(i, rpc, client)

    return {"body": {"message": "Success!"}}
