# lazygit_rocker

## Continuous Integration Status

[![Ci](https://github.com/blooop/lazygit_rocker/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/blooop/lazygit_rocker/actions/workflows/ci.yml?query=branch%3Amain)
[![Codecov](https://codecov.io/gh/blooop/lazygit_rocker/branch/main/graph/badge.svg?token=Y212GW1PG6)](https://codecov.io/gh/blooop/lazygit_rocker)
[![GitHub issues](https://img.shields.io/github/issues/blooop/lazygit_rocker.svg)](https://GitHub.com/blooop/lazygit_rocker/issues/)
[![GitHub pull-requests merged](https://badgen.net/github/merged-prs/blooop/lazygit_rocker)](https://github.com/blooop/lazygit_rocker/pulls?q=is%3Amerged)
[![GitHub release](https://img.shields.io/github/release/blooop/lazygit_rocker.svg)](https://GitHub.com/blooop/lazygit_rocker/releases/)
[![License](https://img.shields.io/github/license/blooop/lazygit_rocker)](https://opensource.org/license/mit/)
[![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/downloads/)
[![Pixi Badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json)](https://pixi.sh)


## Intro

This is a [rocker](https://github.com/tfoote/rocker) extension for adding [lazygit](https://github.com/jesseduffield/lazygit) to a docker container.  Check out the [rocker](https://github.com/osrf/rocker) GitHub page for more details on how Rocker and its extensions work. In short, Rocker allows you to add custom capabilities to existing Docker containers.

## Installation

```
pip install lazygit-rocker
```

## Usage

To install lazygit in a container use the `--lazygit` flag

```
#add pixi to the ubuntu:22.04 image
rocker --lazygit ubuntu:22.04

# add lazygit to the nvidia/cuda image
rocker --lazygit nvidia/cuda
```

