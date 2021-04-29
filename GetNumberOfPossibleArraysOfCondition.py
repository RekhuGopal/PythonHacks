# Python program for implementation 
# check criteria
def checkcriteria(arr):
    w = 0
    for i in range(0,len(arr),1):
    	if i%arr[i] == 0 or arr[i]%i == 0:
    		w=w+1
    if w > 0:
    	return 1
    else:
    	return 0	
    	
# Find combinations 		
def bubbleSort(arr): 
    matches = 0
    n = len(arr) 
    # Traverse through all array elements 
    for i in range(n): 
        # Last i elements are already in place 
        for j in range(0, n-i-1): 
            # traverse the array from 0 , n-i-1
                arr[j], arr[j+1] = arr[j+1], arr[j]
                result = checkcriteria(arr)
                if result == 1:
                    matches = matches+1
    return matches
                    
#create an array
def createAnArray(m):
	createdarray = []
	if m >1 and m < 20:
		for i in range (1,m,1):
		    createdarray.append(i)
	else:
		print ("Given number is out of range")
	return createdarray

# Driver code to test above 
arr = createAnArray(4)
print (arr)
outputvalue = bubbleSort(arr) 
print ("matches found are {}".format(outputvalue+1 ))  
