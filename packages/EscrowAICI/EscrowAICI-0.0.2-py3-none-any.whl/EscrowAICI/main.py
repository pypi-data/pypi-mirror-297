# EscrowAI Python script
# for Algorithm Owner
# Copyright 2023 BeeKeeperAI(r)
# Last updated: 2023-12-01


# Import BeeKeeperAI EscrowAI Python library
from EscrowAI import EscrowAI
import os
import argparse
import base64

if __name__ == "__main__":
    # Example usage:
    # You would call `encrypt_algo` here with the appropriate arguments.
    # This would be done when you run this script from the command line or a GitHub Action step.

    # Retrieve the encryption key from an environment variable or command line argument
    # encryption_key = os.getenv('ENCRYPTION_KEY') or b'some-default-key'

    # username = os.getenv('BEEKEEPER_USERNAME')
    # password = os.getenv('BEEKEEPER_PASSWORD')
    auth_key = os.getenv("private_key")
    project_id = os.getenv("BEEKEEPER_PROJECT_ID")
    environment = os.getenv(
        "BEEKEEPER_ENVIRONMENT", "prod"
    )  # Default to 'prod' if not specified
    # We might need to check organization participation on project..
    organization_id = os.getenv("BEEKEEPER_ORGANIZATION_ID")

    escrow = EscrowAI(
        authKey=auth_key,
        project_id=project_id,
        environment=environment,
        organization_id=organization_id,
    )

    parser = argparse.ArgumentParser(
        description="Encrypt files and package them into a zip archive."
    )
    parser.add_argument(
        "folder", type=str, help="The folder path containing the files to encrypt"
    )
    parser.add_argument(
        "--key", type=str, help="The encryption key (base64 encoded)", required=False
    )
    args = parser.parse_args()

    # Determine the path for the secret.key file
    # key_file_path = os.path.join(os.path.dirname(__file__), 'secret.key')
    # print(key_file_path)

    # Convert base64 key if provided, otherwise generate a random key
    if args.key:
        key = base64.b64decode(args.key)
    else:
        encoded_key = os.environ.get("CONTENT_ENCRYPTION_KEY")
        decoded_key = base64.b64decode(encoded_key)
        # with open(key_file_path, 'rb') as read:
        #   key = read.read()
        # print(key)

    # Call the function with the path to the folder and the encryption key
    escrow.encrypt_algo(args.folder)

    # Example of using a method
    escrow.upload_algorithm(
        os.path.basename(args.folder) + ".zip",
        "covid demo algorithm",
        "validation",
        version="V2",
    )
