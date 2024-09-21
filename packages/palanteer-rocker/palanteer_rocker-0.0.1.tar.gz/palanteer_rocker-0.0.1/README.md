# palanteer_rocker

## Continuous Integration Status

[![Ci](https://github.com/blooop/palanteer_rocker/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/blooop/palanteer_rocker/actions/workflows/ci.yml?query=branch%3Amain)
[![Codecov](https://codecov.io/gh/blooop/palanteer_rocker/branch/main/graph/badge.svg?token=Y212GW1PG6)](https://codecov.io/gh/blooop/palanteer_rocker)
[![GitHub issues](https://img.shields.io/github/issues/blooop/palanteer_rocker.svg)](https://GitHub.com/blooop/palanteer_rocker/issues/)
[![GitHub pull-requests merged](https://badgen.net/github/merged-prs/blooop/palanteer_rocker)](https://github.com/blooop/palanteer_rocker/pulls?q=is%3Amerged)
[![GitHub release](https://img.shields.io/github/release/blooop/palanteer_rocker.svg)](https://GitHub.com/blooop/palanteer_rocker/releases/)
[![License](https://img.shields.io/github/license/blooop/palanteer_rocker
)](https://opensource.org/license/mit/)
[![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/downloads/)
[![Pixi Badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json)](https://pixi.sh)


## Intro

This is a [rocker](https://github.com/tfoote/rocker) extension for adding [palanteer](https://github.com/dfeneyrou/palanteer) to a docker container.  Check out the [rocker](https://github.com/osrf/rocker) GitHub page for more details on how rocker and its extensions work. In short, rocker allows you to add custom capabilities to existing docker images.

## Installation

```
pip install palanteer-rocker
```

## Usage

To install palanteer in an image use the `--palanteer` flag

```
#add palanteer to the ubuntu:22.04 image
rocker --palanteer ubuntu:22.04

# add palanteer to the nvidia/cuda image
rocker --palanteer nvidia/cuda
```

Note that the above example will install palanteer but not work out of the box because the container will not have the correct graphics settings.

To try a fully working example with graphics install [rockerc](https://github.com/blooop/rockerc)


```bash
$ pip install rockerc
# move into the palanteer_rocker folder which contains a rockerc.yaml file with arguments for setting up graphics (and palanteer)
$ cd palanteer_rocker  
# launch rocker with graphics and palanteer flags 
$ rockerc
```

inside the container
```
$ palanteer
```



