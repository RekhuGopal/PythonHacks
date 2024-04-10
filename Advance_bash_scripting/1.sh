#!/bin/bash

# Print a welcome message
echo "Welcome to the Advanced Bash Scripting Interview Preparation Script!"
echo "Let's get started..."

# Check if the script is running as root
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root"
    exit 1
fi

# Print the current date and time
echo "Current date and time: $(date)"

# Print the system information
echo "System information:"
uname -a

# List all installed packages
echo "Installed packages:"
if command -v dpkg &> /dev/null; then
    dpkg --list
elif command -v rpm &> /dev/null; then
    rpm -qa
else
    echo "Unable to determine package manager"
fi

# Check the disk space
echo "Disk space:"
df -h

# Check the memory usage
echo "Memory usage:"
free -m

# Print a closing message
echo "Script execution completed. Goodbye!"
