import os
import requests
import boto3
import datetime


def load_anvil_state(rpc, data):
    response = requests.post(f"http://{rpc}", json={
        "jsonrpc": "2.0",
        "method": "anvil_loadState",
        "params": [data],
        "id": 1
    })
    return response.json()


def read_state(obj_path):
    # configure the Digital Ocean Spaces client
    session = boto3.session.Session()
    client = session.client(
        "s3",
        region_name="nyc3",
        endpoint_url="https://nyc3.digitaloceanspaces.com",
        aws_access_key_id=os.environ["SPACES_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["SPACES_SECRET_ACCESS_KEY"]
    )

    # read the state from the latest backup
    response = client.get_object(
        Bucket=os.environ['SPACES_BUCKET_NAME'],
        Key=obj_path
    )
    state_hex = response['Body'].read().decode('utf-8')
    return state_hex


def main(args):
    id = args.get('id', 0)
    backup_path = args.get('backup_path')
    name = args.get("name", "LOAD")
    greeting = "Hello " + name + "!"
    print(greeting)
    return {"body": greeting}
  