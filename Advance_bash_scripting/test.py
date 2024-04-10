from collections import defaultdict

def find_anagrams(words):
    # Create a defaultdict to store anagrams
    anagrams = defaultdict(list)
    
    # Iterate through each word in the list
    for word in words:
        # Sort the characters in the word
        sorted_word = ''.join(sorted(word))
        
        # Add the word to the list of anagrams with the sorted word as key
        anagrams[sorted_word].append(word)
    
    # Filter out non-anagram groups
    return [group for group in anagrams.values() if len(group) > 1]

# Example usage:
word_list = ["listen", "silent", "hello", "world", "act", "cat", "dog", "god"]
#out = [[],[]]
anagram_groups = find_anagrams(word_list)
print("Anagram groups:")

print(anagram_groups)
