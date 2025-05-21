#!/bin/bash

# Navigate to the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Loop through values for --pb and --pt
for pb in 1 10 100 1000 10000 100000; do
    for pt in 0 1 10; do
        # Run pub.py with arguments
        python3 pub.py --node 1 --mt 100 --pb "$pb" --pt "$pt" --config config.json \
        --ping_dev orin --pong_dev orin --inter_dev orin \
        --struct single
    done
done