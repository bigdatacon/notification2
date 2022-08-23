#!/bin/sh

python3 ./wait_for_pg.py
python3 ./wait_for_kafka.py
python3 ./main.py

exec "$@"