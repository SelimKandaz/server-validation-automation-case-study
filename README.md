# Server Validation Automation Case Study

A write-up of how I approach server validation: hardware check-in, firmware update decisions, quick proof testing, evidence capture, and technician-readable reports. It comes with two small read-only scripts.

## Scripts

Linux snapshot:

```bash
chmod +x scripts/server_validation_snapshot.sh
./scripts/server_validation_snapshot.sh
```

Redfish drive serial probe:

```bash
python scripts/redfish_drive_serial_probe.py
```

Both are read-only. They don't update firmware, clear logs, or reset anything.

See also [CNServerOps](https://github.com/SelimKandaz/CNServerOps).

## License

MIT
