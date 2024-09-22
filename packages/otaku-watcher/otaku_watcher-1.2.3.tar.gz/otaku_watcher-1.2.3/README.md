<div align="center">

  # otaku-watcher
  <sub>A mov-cli plugin for watching anime.</sub>

  [![Pypi Version](https://img.shields.io/pypi/v/otaku-watcher?style=flat)](https://pypi.org/project/otaku-watcher)

  <img src="https://github.com/JDALab/otaku-watcher/assets/123201787/2df8d707-b472-48b3-aaa1-f6d5154c686d">

</div>

> [!CAUTION]
> We are on the lookout for maintainers and if we don't find any soon this project may become unmaintained! Please consider or nominate a friend. Thank you.

## Installation
Here's how to install and add the plugin to mov-cli.

1. Install the pip package.
```sh
pip install otaku-watcher
```
2. Then add the plugin to your mov-cli config.
```sh
mov-cli -e
```
```toml
[mov-cli.plugins]
anime = "otaku-watcher"
```

## Usage
```sh
mov-cli -s anime lycoris recoil
```
