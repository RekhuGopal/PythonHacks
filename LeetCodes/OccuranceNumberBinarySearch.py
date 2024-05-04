numbers = [1,4,6,9,11,15,15,15,17,21,34,34,56]
number_to_find = 15

def binary_search (list , numberToFind):

    li = 0
    ri = len(list) - 1
    
    while li <= ri:
        mi = (li + ri) // 2
        if numberToFind == list[mi]:
            return mi
        
        if list[mi] < numberToFind:
           li = mi + 1
        else:
           ri = mi -1
    return - 1

def find_occurances (list , numberTofind):
    index =  binary_search (list , numberTofind)
    print(index)
    NumberIndexes = [index]
    i = index -1
    while i >= 0:
        if list[i] == numberTofind:
            NumberIndexes.append(i)
        i -= 1

    i = index +1 
    while i < len(list):
        if list[i] == numberTofind:
            NumberIndexes.append(i)
        i += 1
    return sorted(NumberIndexes)


print(find_occurances(numbers, 15))