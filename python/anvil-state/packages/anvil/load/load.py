import os
import requests
import boto3
import base64


def authorize(auth_str):
    """
    Validate a basic auth hash ("Basic <base64 encoded string>") against
    the BASIC_AUTH_USER and BASIC_AUTH_PASSWORD environment variables.

    :param auth_str: The authorization string to validate
    :return: True if the authorization string is valid, False otherwise
    """
    basicAuth = base64.b64decode(auth_str.split(" ")[1]).decode("utf-8")
    username, password = basicAuth.split(":")

    return username == os.environ["BASIC_AUTH_USER"] and password == os.environ["BASIC_AUTH_PASSWORD"]


def load_anvil_state(rpc, data):
    """
    Load the state of an Anvil process via a data hex string
    :param rpc: The RPC address
    :param data: The data hex string

    :return: The response from the RPC call
    """
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
    """
    Load the state of an Anvil process from a backup file in Digital Ocean Spaces

    **Requires Basic Auth**

    :param args.id: The ID of the Anvil process to load the state for
    :param args.backup_path: Optional - The path to the backup file in Digital Ocean Spaces
    """
    authorization = args["__ow_headers"].get("authorization", "")
    authorize(authorization)
    if not authorize(authorization):
        return {
            "statusCode": 401,
            "body": {
                "message": "Invalid Basic Auth credentials",
                "success": False
            }
        }
    
    id = args.get('id', 0)
    backup_path = args.get('backup_path')
    state_hex = read_state(backup_path if backup_path else f"latest/anvil{id}.txt")
    result = load_anvil_state(os.environ['RPCS'].split(',')[id], state_hex)
    return {"body": result}
