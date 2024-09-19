#!/bin/bash

# Verify correct usage
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <number_of_times>"
    exit 1
fi

num_times=$1

# Run PlayMaker.py num_times times
for i in $(seq 1 "$num_times"); do
    python3 PlayMaker.py
done
