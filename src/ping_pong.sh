#!/bin/bash
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
payload_sizes=(1 10 100 1000 10000 100000 1000000)
# payload_sizes=(10000000)
pingpong_times=(0 1 10)
protocols=(zenoh mqtt)
date=$(date +"%Y-%m-%d")

for protocol in "${protocols[@]}"; do
    for pb in "${payload_sizes[@]}"; do
        for pt in "${pingpong_times[@]}"; do
            python3 $SCRIPT_DIR/process_measurement_helper.py --protocol $protocol --dn "$protocol/$date" --pb $pb --pt $pt
        done
    done
done