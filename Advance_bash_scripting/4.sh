#!/bin/bash

# Loop through numbers and print them
for i in {1..5}; do
    echo "Number: $i"
done

# Check if a number is even or odd
number=6
if [ $((number % 2)) -eq 0 ]; then
    echo "$number is even"
else
    echo "$number is odd"
fi
