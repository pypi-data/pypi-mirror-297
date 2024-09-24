# geysermc

![Tests](https://github.com/legopitstop/geysermc/actions/workflows/tests.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/geysermc)](https://pypi.org/project/geysermc/)
[![Python](https://img.shields.io/pypi/pyversions/geysermc)](https://www.python.org/downloads//)
![Downloads](https://img.shields.io/pypi/dm/geysermc)
![Status](https://img.shields.io/pypi/status/geysermc)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Issues](https://img.shields.io/github/issues/legopitstop/geysermc)](https://github.com/legopitstop/geysermc/issues)

The unofficial Python wrapper for geysermc.org

## Installation

Install the module with pip:

```bat
pip3 install geysermc
```

Update existing installation: `pip3 install geysermc --upgrade`

## Links

- [Documentation](https://docs.lpsmods.dev/geysermc)
- [Source Code](https://github.com/legopitstop/geysermc)

## Requirements

| Name                                             | Description                                      |
| ------------------------------------------------ | ------------------------------------------------ |
| [`Pillow`](https://pypi.org/project/pillow/)     | Python Imaging Library (Fork)                    |
| [`requests`](https://pypi.org/project/requests/) | Requests is a simple, yet elegant, HTTP library. |
| [`pydantic`](https://pypi.org/project/pydantic/) | Data validation using Python type hints          |

## Features

- Get Microsoft xuid or gamertag.
- Download any geyser project.
- Get bedrock skin.

## Examples

Show bedrock player skin

```Python
from geysermc import GeyserMC

api = GeyserMC()

xuid = api.get_xuid('legopitstop')
skin = api.get_skin(xuid)
image = api.get_raw_texture(skin.texture_id)
image.show()
```

Download Geyser plugin

```Python
from geysermc import GeyserMC

api = GeyserMC()

with open('geyser-spigot.jar', 'wb') as fd:
    data = api.get_download('geyser', 'spigot')
    fd.write(data)
```
