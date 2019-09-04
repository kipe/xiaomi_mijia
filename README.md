# Xiaomi Mijia
> A simple and clean Python library for
[Xiaomi temperature and humidity sensors](https://xiaomi-store.cz/en/temperature-sensors/612-xiaomi-temperature-and-humidity-sensor-6934177702709.html)

## Installation
As the library is based on [bluepy](https://github.com/IanHarvey/bluepy),
compilation of `bluepy-helper` is required. This requires `glib2` development
packages.

On Debian-based systems the installation goes a bit like:

```sh
sudo apt-get install libglib2.0-dev
pip install git+https://github.com/kipe/xiaomi_mijia.git
```
