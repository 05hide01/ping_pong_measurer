#!/bin/bash

payload_sizes=(1 10 100 1000 10000 100000 1000000)
# payload_sizes=(10000000)
pingpong_times=(0 1 10)

for pb in "${payload_sizes[@]}"; do
    for pt in "${pingpong_times[@]}"; do
        python3 process_measurement_helper.py --dn kakip_kakip_sh --pb $pb --pt $pt
    done
done