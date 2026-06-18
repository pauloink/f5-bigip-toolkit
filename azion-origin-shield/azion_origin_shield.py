#!/usr/bin/env python3

import os
import subprocess
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv()

AZION_API_URL = "https://api.azionapi.net"
AZION_BASIC_AUTH = os.getenv("AZION_BASIC_AUTH")
NETWORK_LIST_ID = os.getenv("NETWORK_LIST_ID", "187")

DATA_GROUP_NAME = os.getenv(
    "DATA_GROUP_NAME",
    "ext_dg_azion_origin_shield",
)

OUTPUT_FILE = Path(
    os.getenv(
        "OUTPUT_FILE",
        "/root/ext_dg_azion_origin_shield.txt",
    )
)

REQUEST_TIMEOUT = 30


def validate_configuration():
    if not AZION_BASIC_AUTH:
        raise RuntimeError(
            "AZION_BASIC_AUTH was not found in the .env file"
        )

    if not NETWORK_LIST_ID.isdigit():
        raise RuntimeError("NETWORK_LIST_ID must contain only numbers")


def get_azion_token(session):
    response = session.post(
        f"{AZION_API_URL}/tokens",
        headers={
            "Accept": "application/json; version=3",
            "Authorization": f"Basic {AZION_BASIC_AUTH}",
        },
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()
    token = response.json().get("token")

    if not token:
        raise RuntimeError(
            "The Azion API response did not contain an authentication token"
        )

    return token


def get_origin_shield_addresses(session, token):
    response = session.get(
        f"{AZION_API_URL}/network_lists/{NETWORK_LIST_ID}",
        headers={
            "Accept": "application/json; version=3",
            "Authorization": f"Token {token}",
        },
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()
    data = response.json()

    addresses = (
        data.get("results", {})
        .get("items_values", [])
    )

    if not addresses:
        raise RuntimeError(
            "The Azion network list did not contain any addresses"
        )

    return addresses


def write_data_group_file(addresses):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    temporary_file = OUTPUT_FILE.with_suffix(
        f"{OUTPUT_FILE.suffix}.tmp"
    )

    with temporary_file.open(
        "w",
        encoding="utf-8",
        newline="\n",
    ) as file:
        for address in addresses:
            file.write(f"network {address},\n")

    temporary_file.replace(OUTPUT_FILE)

    print(
        f"Wrote {len(addresses)} addresses to {OUTPUT_FILE}"
    )


def update_bigip_data_group():
    command = [
        "tmsh",
        "modify",
        "sys",
        "file",
        "data-group",
        DATA_GROUP_NAME,
        "source-path",
        f"file:{OUTPUT_FILE}",
    ]

    subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )

    print(f"Updated BIG-IP data group: {DATA_GROUP_NAME}")


def main():
    validate_configuration()

    try:
        with requests.Session() as session:
            token = get_azion_token(session)

            addresses = get_origin_shield_addresses(
                session,
                token,
            )

        write_data_group_file(addresses)
        update_bigip_data_group()

        print("Azion Origin Shield update completed successfully.")

    except requests.exceptions.Timeout as error:
        raise RuntimeError(
            f"The Azion API request timed out after "
            f"{REQUEST_TIMEOUT} seconds"
        ) from error

    except requests.exceptions.HTTPError as error:
        raise RuntimeError(
            f"The Azion API returned an HTTP error: {error}"
        ) from error

    except requests.exceptions.ConnectionError as error:
        raise RuntimeError(
            f"Could not connect to the Azion API: {error}"
        ) from error

    except requests.exceptions.JSONDecodeError as error:
        raise RuntimeError(
            "The Azion API returned an invalid JSON response"
        ) from error

    except subprocess.CalledProcessError as error:
        details = error.stderr.strip() if error.stderr else str(error)

        raise RuntimeError(
            f"Failed to update the BIG-IP data group: {details}"
        ) from error


if __name__ == "__main__":
    main()
