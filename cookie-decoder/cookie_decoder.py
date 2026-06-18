#!/usr/bin/env python3

import re
import struct
from urllib.parse import urlparse

import requests


REQUEST_TIMEOUT = 10


def normalize_url(value):
    if not value.startswith(("http://", "https://")):
        value = f"https://{value}"

    parsed = urlparse(value)

    if not parsed.hostname:
        raise ValueError("Invalid URL")

    return value


def decode_cookie(cookie_value):
    try:
        host, port, _ = cookie_value.split(".", maxsplit=2)
        ip_address = ".".join(
            str(octet) for octet in struct.pack("<I", int(host))
        )

        packed_port = struct.pack("<I", int(port))
        decoded_port = packed_port[0] * 256 + packed_port[1]

        return ip_address, decoded_port

    except (ValueError, struct.error) as error:
        raise ValueError(
            "The BIG-IP cookie contains an unsupported value"
        ) from error


def inspect_url(target_url):
    response = requests.head(
        target_url,
        allow_redirects=False,
        timeout=REQUEST_TIMEOUT,
    )

    if response.is_redirect:
        redirect_url = response.headers.get("Location", "Unknown")
        print(f"Redirect detected: {redirect_url}")
        return

    print(f"HTTP status: {response.status_code}")

    set_cookie = response.headers.get("Set-Cookie")

    if not set_cookie:
        print("No Set-Cookie header was found in the response.")
        return

    cookie_match = re.search(
        r"BIGipServer([^=;]+)=([^;]+)",
        set_cookie,
        re.IGNORECASE,
    )

    if not cookie_match:
        print(
            "No decodable BIG-IP persistence cookie was found. "
            "The cookie may be encrypted or use a different format."
        )
        return

    pool_name = cookie_match.group(1)
    cookie_value = cookie_match.group(2)

    ip_address, port = decode_cookie(cookie_value)

    print(f"Pool name: {pool_name}")
    print(f"Pool member: {ip_address}:{port}")


def main():
    user_input = input("URL or hostname: ").strip()

    try:
        target_url = normalize_url(user_input)
        inspect_url(target_url)

    except ValueError as error:
        print(f"Invalid input: {error}")

    except requests.exceptions.Timeout:
        print(
            f"The request timed out after {REQUEST_TIMEOUT} seconds."
        )

    except requests.exceptions.SSLError:
        print("TLS certificate validation failed.")

    except requests.exceptions.ConnectionError:
        print("Could not connect to the target.")

    except requests.exceptions.RequestException as error:
        print(f"Request failed: {error}")


if __name__ == "__main__":
    main()
