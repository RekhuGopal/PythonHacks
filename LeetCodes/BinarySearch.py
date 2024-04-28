a = [4,9,11,17,21,25,29,32,38]
# liner search is O(n)
# binary search is log(n)
'''
def linear_search(listToSearch, NumberTofind):
    for index , element in listToSearch:
        if element == NumberTofind:
            return index
        return -1
'''

def binary_search(listToSearch, NumberTofind):

    li = 0
    ri = len(listToSearch) - 1
    mi = 0

    while li <= ri:
        mi = (li + ri) // 2
        mn = listToSearch[mi]
        if mn == NumberTofind:
            return mi
        if mn < NumberTofind:
            li = mi +1
        else:
            ri = mi -1
    return -1

print(binary_search(a , 17))
        
