# jkGlyphsHelpers Installation

Usually, `jkGlyphsHelpers` will be installed automatically when you install Jens
Kutilek’s Glyphs Scripts through the plugin manager.

## Installation via pip

For all pip installs, make sure to call the `pip` command that corresponds to the Python
version you have selected in Glyphs’ settings. You may have to add the Python version
to the command, e.g. `pip3.12`, `pip3.13`, etc.

### Install the latest release from PyPI

```bash
pip install --user jkglyphshelpers
```

## Installation from the GitHub repository

For development or when you need an unreleased version.

```bash
git clone https://github.com/jenskutilek/jkGlyphsHelpers.git
cd jkGlyphsHelpers
pip install --user .
```
