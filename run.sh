#!/usr/bin/env bash

set -e

python3 publisher.py &
python3 subscriber.py &
python3 statistics.py &