def insertion_sort (element):
    for i in range(1, len(element)):
        anchor = element[i]
        j = i - 1
        while j >= 0 and anchor < element[j]:
            element[j+1] = element[j]
            j = j-1
        element[j+1] = anchor
    return element

if __name__ == '__main__':
    elements = [11, 9, 29,7, 2, 15, 28]
    insertion_sort(elements)
    print(elements)
