# F5 BIG-IP Cookie Decoder

A Python utility that inspects an HTTP response and decodes an unencrypted F5 BIG-IP persistence cookie.

When the supported cookie format is present, the tool displays the associated pool name, destination IP address and service port.

## Features

- Detects unencrypted `BIGipServer` persistence cookies
- Extracts the F5 pool name
- Decodes the destination IP address and port
- Detects HTTP redirects
- Validates TLS certificates by default
- Handles connection, timeout and malformed-cookie errors

## Requirements

- Python 3.10+
- Network access to the authorized target
- An unencrypted F5 BIG-IP persistence cookie

## Installation

From the repository root:

```bash
cd cookie-decoder
python -m venv .venv
```

Activate the environment and install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python cookie_decoder.py
```

Enter an authorized URL or hostname:

```text
URL or hostname: example.com
```

Example output:

```text
HTTP status: 200
Pool name: example_pool
Pool member: 192.0.2.10:443
```

All values shown above are fictional examples.

## Limitations

- Encrypted cookies cannot be decoded by this utility.
- Other BIG-IP cookie formats may use different encoding.
- Some applications do not return cookies in response to HEAD requests.
- Results should be validated before being used for troubleshooting.

## Security

Use this tool only against systems where you have explicit authorization.

Decoded cookies may reveal internal addressing information. Do not publish real output, screenshots or infrastructure details.

## Reference

The decoding format is based on F5 documentation:

- [Overview of BIG-IP persistence cookie encoding](https://my.f5.com/manage/s/article/K6917)

## Disclaimer

This project is not affiliated with or endorsed by F5. Use it only for authorized administration, troubleshooting and security testing.
