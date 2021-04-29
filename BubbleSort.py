# Python program for implementation of Bubble Sort 
def bubbleSort(arr): 
    n = len(arr) 
    # Traverse through all array elements 
    for i in range(n): 
        # Last i elements are already in place 
        for j in range(0, n-i-1): 
            # traverse the array from 0 to n-i-1 
            # Swap if the element found is >
            # than the next element 
            if arr[j] > arr[j+1] : 
                arr[j], arr[j+1] = arr[j+1], arr[j] 
                print ("--:Array:--")
                for i in range(len(arr)): 
                    print ("%d" %arr[i])

# Driver code to test above 
arr = [1,2,3] 
bubbleSort(arr) 
print ("Sorted array outside is:") 
for i in range(len(arr)): 
    print ("%d" %arr[i])
