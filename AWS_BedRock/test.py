my_list = [1, 2, 3]
my_list.append(4)
print(my_list)  # Output: [1, 2, 3, 4]

# Appending another list as an element
another_list = [5, 6, 7]
my_list.append(another_list)
print(my_list)  # Output: [1, 2, 3, 4, [5, 6, 7]]

my_list = [1, 2, 3]
another_list = [4, 5, 6]

my_list.extend(another_list)
print(my_list)  # Output: [1, 2, 3, 4, 5, 6]

# Extend with a string (iterable)
my_list.extend("hello")
print(my_list)  # Output: [1, 2, 3, 4, 5, 6, 'h', 'e', 'l', 'l', 'o']
