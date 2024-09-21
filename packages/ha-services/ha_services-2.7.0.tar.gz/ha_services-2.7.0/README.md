# ha_services

[![tests](https://github.com/jedie/ha_services/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/jedie/ha_services/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/ha_services/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/ha_services)
[![ha_services @ PyPi](https://img.shields.io/pypi/v/ha_services?label=ha_services%20%40%20PyPi)](https://pypi.org/project/ha_services/)
[![Python Versions](https://img.shields.io/pypi/pyversions/ha_services)](https://github.com/jedie/ha_services/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/ha_services)](https://github.com/jedie/ha_services/blob/main/LICENSE)

Helpers to send periodic information via MQTT to Home Assistant

* https://pypi.org/project/ha-services/

Use by:

* https://github.com/jedie/tinkerforge2mqtt
* https://github.com/jedie/victron-ble2mqtt
* https://github.com/jedie/energymeter2mqtt
* https://github.com/jedie/pysmartmeter

# start development

```bash
~$ git clone https://github.com/jedie/ha-services.git
~$ cd inverter-connect
~/ha-services$ ./dev-cli.py --help
```


# dev CLI

[comment]: <> (✂✂✂ auto generated dev help start ✂✂✂)
```
Usage: ./dev-cli.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ check-code-style            Check code style by calling darker + flake8                          │
│ coverage                    Run tests and show coverage report.                                  │
│ fix-code-style              Fix code style of all ha_services source code files via darker       │
│ install                     Run pip-sync and install 'ha_services' via pip as editable.          │
│ mypy                        Run Mypy (configured in pyproject.toml)                              │
│ pip-audit                   Run pip-audit check against current requirements files               │
│ publish                     Build and upload this project to PyPi                                │
│ test                        Run unittests                                                        │
│ tox                         Run tox                                                              │
│ update                      Update "requirements*.txt" dependencies files                        │
│ update-test-snapshot-files  Update all test snapshot files (by remove and recreate all snapshot  │
│                             files)                                                               │
│ version                     Print version and exit                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated dev help end ✂✂✂)


# DEMO app CLI

[comment]: <> (✂✂✂ auto generated app help start ✂✂✂)
```
Usage: ./cli.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ edit-settings         Edit the settings file. On first call: Create the default one.             │
│ print-settings        Display (anonymized) MQTT server username and password                     │
│ publish-loop          Publish data via MQTT for Home Assistant (endless loop)                    │
│ systemd-debug         Print Systemd service template + context + rendered file content.          │
│ systemd-remove        Write Systemd service file, enable it and (re-)start the service. (May     │
│                       need sudo)                                                                 │
│ systemd-setup         Write Systemd service file, enable it and (re-)start the service. (May     │
│                       need sudo)                                                                 │
│ systemd-status        Display status of systemd service. (May need sudo)                         │
│ systemd-stop          Stops the systemd service. (May need sudo)                                 │
│ test-mqtt-connection  Test connection to MQTT Server                                             │
│ version               Print version and exit                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated app help end ✂✂✂)


# Backwards-incompatible changes
## v2.0.0

Complete refactor of `mqtt4homeassistant` module.
New usage, see: `ha_services/example.py`
