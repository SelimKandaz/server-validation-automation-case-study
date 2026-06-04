# Customization Guide

This project can be adapted for safe, read-only server validation workflows.

## Common customization points

- Hardware inventory commands
- Redfish probe targets
- Report format
- Pass/review/fail rules
- Support bundle references
- Technician checklist language

## Start here

- `scripts/server_validation_snapshot.sh`
- `scripts/redfish_drive_serial_probe.py`
- `docs/workflow.md`

## Safety boundary

This public project intentionally avoids destructive actions such as firmware application, log clearing and management-controller resets.
