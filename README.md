# F5 BIG-IP Toolkit

Python scripts and utilities for F5 BIG-IP administration, automation and troubleshooting.

## Tools

### Cookie Decoder

Decodes F5 BIG-IP persistence cookies to identify the encoded destination server and service port.

- [Documentation](./cookie-decoder/)
- Language: Python
- Purpose: Assist with persistence troubleshooting and traffic analysis

### External Data Group Automation

Automates the creation or update of external data groups used by F5 BIG-IP configurations.

- [Documentation](./external-data-group/)
- Language: Python
- Purpose: Automate external data group management and reduce manual configuration

### General Scripts

Additional scripts and utilities for F5 BIG-IP administration and troubleshooting.

- [Documentation](./general-scripts/)
- Language: Shell and configuration files
- Purpose: Centralize reusable operational tools for F5 BIG-IP environments

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
