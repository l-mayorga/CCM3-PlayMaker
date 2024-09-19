#!/bin/bash

# Check if the number of iterations is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <number_of_times>"
    exit 1
fi

# Get the number of times to run the script
num_times=$1

# Loop to execute the PlayMaker.py script
for i in $(seq 1 "$num_times"); do
    python3 PlayMaker.py
done
