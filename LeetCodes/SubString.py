def is_perfect_substring(substring, k):
    count = [0] * 10  # Initialize a frequency array for digits 0 to 9

    # Count the frequency of each digit in the substring
    for digit in substring:
        count[int(digit)] += 1

    # Check if all digits occur exactly k times
    return all(c == k for c in count)


def count_perfect_substrings(s, k):
    n = len(s)
    count = 0  # Initialize count of perfect substrings

    # Iterate through each character in the string
    for i in range(n):
        freq = [0] * 10  # Initialize frequency array for each new starting index i
        for j in range(i, n):
            # Update frequency of digit at index j
            freq[int(s[j])] += 1

            # Check if all digits occur exactly k times in the current substring
            if all(c == k for c in freq):
                count += 1

    return count


# Example usage
s = "1102021222"
k = 2
print("Number of perfect substrings:", count_perfect_substrings(s, k))
