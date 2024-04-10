#!/bin/bash

# Create a directory if it doesn't exist
mkdir -p /path/to/directory

# Check if a file exists
if [ -f "/path/to/file" ]; then
    echo "File exists"
else
    echo "File does not exist"
fi

# List files in a directory
echo "Files in directory:"
ls /path/to/directory

# Count the number of files in a directory
file_count=$(ls /path/to/directory | wc -l)
echo "Number of files: $file_count"
