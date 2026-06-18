# F5 BIG-IP Toolkit

Python scripts and utilities for F5 BIG-IP administration, automation and troubleshooting.

## Tools

### Cookie Decoder

Decodes F5 BIG-IP persistence cookies to identify the encoded destination server and service port.

- [Documentation](./cookie-decoder/)
- Language: Python
- Purpose: Assist with persistence troubleshooting and traffic analysis

### Azion Origin Shield Updater

Retrieves updated Azion Origin Shield addresses through the Azion API and updates an external data group on F5 BIG-IP.

- [Documentation](./azion-origin-shield/)
- Language: Python
- Purpose: Keep F5 BIG-IP synchronized with changing Azion Origin Shield addresses


## Requirements

Requirements vary by tool. See the documentation inside each directory for installation and configuration instructions.

General requirements may include:

- Python 3.10+
- Access to an authorized F5 BIG-IP environment
- Valid credentials or API tokens
- Network access to the target environment

## Installation

Clone the repository:

```bash
git clone https://github.com/pauloink/f5-bigip-toolkit.git
cd f5-bigip-toolkit
