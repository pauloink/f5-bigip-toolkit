### Azion Origin Shield Updater

Retrieves updated Azion Origin Shield addresses through the Azion API and integrates them with F5 BIG-IP configurations.

- [Documentation](./azion-origin-shield/)
- Language: Python
- Purpose: Keep F5 BIG-IP configurations synchronized with changing Azion Origin Shield addresses

## First-time BIG-IP setup

The script updates an existing BIG-IP external data group. Before the first execution, create the imported data group file:

```bash
tmsh create sys file data-group ext_dg_azion_origin_shield \
  source-path file:/root/ext_dg_azion_origin_shield.txt \
  type ip
```

The file and data group names must match the values configured in `.env`:

```env
DATA_GROUP_NAME=ext_dg_azion_origin_shield
OUTPUT_FILE=/root/ext_dg_azion_origin_shield.txt
```

The initial source file must exist before running the creation command.

## Generating the authentication value

The Azion Basic Authentication value is a Base64 representation of:

```text
username:password
```

Generate it without adding a line break:

```bash
printf '%s' 'user@example.com:password' | base64
```

Add only the generated value to your local `.env`:

```env
AZION_BASIC_AUTH=your_base64_encoded_credentials
```

Never publish the generated value or your `.env` file.

## iRule example

The external data group can be used to allow requests originating from the current Azion Origin Shield addresses:

```tcl
when CLIENT_ACCEPTED {
    if { [class match [IP::client_addr] equals ext_dg_azion_origin_shield] } {
        return
    } else {
        drop
    }
}
```

Review and test this policy before associating it with a production Virtual Server. An incorrect or empty data group may block legitimate traffic.

## Scheduling updates

The script can be executed periodically to keep the data group synchronized with Azion.

Example cron entry for an hourly update:

```cron
0 * * * * cd /path/to/azion-origin-shield && /usr/bin/python3 azion_origin_shield.py >> /var/log/azion-origin-shield.log 2>&1
```

Adjust the path and update interval for your environment.

BIG-IP upgrades may affect locally installed scripts or scheduled tasks. Document the deployment and verify it after upgrades or configuration restores.
