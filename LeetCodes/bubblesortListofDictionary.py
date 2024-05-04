elements = [
        { 'name': 'mona',   'transaction_amount': 1000, 'device': 'iphone-10'},
        { 'name': 'dhaval', 'transaction_amount': 400,  'device': 'google pixel'},
        { 'name': 'kathy',  'transaction_amount': 200,  'device': 'vivo'},
        { 'name': 'aamir',  'transaction_amount': 800,  'device': 'iphone-8'},
    ]

def bubble_sort(elements, key='name'):
    n = len(elements)
    for i in range(n-1):
        swapped = False
        for j in range(0, n-i-1):
             if elements[j][key] > elements[j+1][key]:
                elements[j] , elements[j+1] = elements[j+1],elements[j]
                swapped = True
        if not swapped:
            break
    return elements           

print(bubble_sort(elements,key='name'))