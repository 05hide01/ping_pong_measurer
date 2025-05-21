#!/bin/bash

# Navigate to the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Loop through values for --pb and --pt
for pb in 1000000; do
    for pt in 10; do
        # Run pub.py with arguments
        python3 pub.py --node 1 --mt 100 --pb "$pb" --pt "$pt" --config config.json \
        --ping_dev rasp5 --pong_dev orin --inter_dev orin \
        --struct broker_w_sub
    done
done
