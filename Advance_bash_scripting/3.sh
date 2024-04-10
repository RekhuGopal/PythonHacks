#!/bin/bash

# Search for a pattern in a file
grep "pattern" /path/to/file

# Replace a string in a file
sed -i 's/old_string/new_string/g' /path/to/file

# Count the number of occurrences of a word in a file
word_count=$(grep -o "word" /path/to/file | wc -l)
echo "Number of occurrences of 'word': $word_count"
