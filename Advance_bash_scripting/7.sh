#!/bin/bash

# Define the bubble sort function
bubble_sort() {
    # Store the array passed as argument
    arr=("$@")
    
    # Get the length of the array
    n=${#arr[@]}
    
    # Perform the bubble sort algorithm
    for ((i = 0; i < n-1; i++)); do
        for ((j = 0; j < n-i-1; j++)); do
            if ((arr[j] > arr[j+1])); then
                # Swap the elements
                temp=${arr[j]}
                arr[j]=${arr[j+1]}
                arr[j+1]=$temp
            fi
        done
    done
    
    # Print the sorted array
    echo "Sorted array: ${arr[@]}"
}

# Example usage:
numbers=(64 34 25 12 22 11 90)
echo "Original array: ${numbers[@]}"
bubble_sort "${numbers[@]}"
