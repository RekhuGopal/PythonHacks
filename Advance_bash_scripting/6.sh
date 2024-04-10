#!/bin/bash

# Initialize a variable
counter=0

# Loop that always executes at least once
while true; do
    # Increment the counter
    ((counter++))
    
    # Print the counter value
    echo "Counter: $counter"
    
    # Check if the counter reaches a certain value
    if [ $counter -eq 5 ]; then
        break  # Exit the loop when the condition is met
    fi
done
