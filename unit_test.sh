#!/bin/zsh

export PWD=$(pwd)
export PYTHONPATH="${PYTHONPATH}:${PWD}"
echo PYTHONPATH=$PYTHONPATH

echo
echo Running unit tests...

# python3 -B tests/other/port_test.py

# python3 -B tests/mapper/mapper_test.py
