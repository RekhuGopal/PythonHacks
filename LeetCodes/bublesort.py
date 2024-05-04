a = [1, 2, 3, 10, 56, 57, 57, 89, 89, 89, 89]

n = len(a)
for i in range(n-1):
    swaped =  False
    for j in range(0,n-i-1):
        if a[j] > a[j+1]:
            a[j] , a[j+1] = a[j+1] , a[j]
            swaped =  True
    if not swaped:
        break

print(a)
