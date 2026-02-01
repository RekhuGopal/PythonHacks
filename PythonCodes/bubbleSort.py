def bubbleSort(arr):
	n = len(arr) 
	while n>1: # Repeat passes until the unsorted part has more than one element

		new_n=0 # Stores the index of the last swap in this pass
		for i in range(1,n):
			if(arr[i-1]>arr[i]): # Check if adjacent elements are in wrong order
				arr[i],arr[i-1]=arr[i-1],arr[i] #swap the elements 
				new_n=i # Update last swapped position
		n=new_n # Reduce the range for the next pass
#example
arr = [64, 34, 25, 12, 22, 11, 90]
print("Before sorting ",arr )
bubbleSort(arr)
print("Sorted array is:")
for i in range(len(arr)):
	print("% d" % arr[i], end=" ")
