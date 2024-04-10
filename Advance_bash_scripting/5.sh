#!/bin/bash

# Define a function
hello() {
    echo "Hello, world!"
}

# Call the function
hello

# Function with arguments
greet() {
    echo "Hello, $1!"
}

# Call the function with an argument
greet "John"
