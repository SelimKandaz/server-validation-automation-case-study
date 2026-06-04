# Server Validation Automation Case Study

An open-source case study and safe toolset for server validation workflows, hardware inventory and report generation.

This repository does not publish destructive update/reset workflows. It includes high-level architecture, sanitized examples and safe read-only demo scripts.

## Safe demo scripts

Linux local snapshot:

```bash
chmod +x scripts/server_validation_snapshot.sh
./scripts/server_validation_snapshot.sh
```

Redfish drive serial probe:

```bash
python scripts/redfish_drive_serial_probe.py
```

The scripts are read-only. They do not apply firmware updates, clear logs, reset management controllers or run destructive tests.

## What this case study covers

- Server hardware check-in workflow
- Firmware/update decision flow
- Offline-first repository concept
- Quick proof hardware validation
- Log evidence capture and cleanup concept
- Support bundle concept
- HTML report portal concept
- Technician-readable output design

## Do not commit

- Real BMC/iDRAC/iLO credentials
- Real generated reports
- Real service tags
- Private inventory data

## License

MIT
