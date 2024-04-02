# Pydantic Benchmarks

This repository is a quick set of scripts to compare `pydantic` implementations through time.

## Usage

The idea is that the `versions/` subdirectory will contain a series of virtualenvs containing different `pydantic` versions. `create-venv.py` is used to set these up.

`sample.py` is used to run the same benchmarks for each of these versions.
