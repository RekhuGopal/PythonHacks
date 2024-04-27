a = [10, 3, 56, 57, 57, 89, 89,89, 89]

large = a[0]
temp = 0
for i in range(1, len(a)):
    if a[i] > large:
       temp = large
       large = a[i]
    else:
        continue
print(temp, large)
