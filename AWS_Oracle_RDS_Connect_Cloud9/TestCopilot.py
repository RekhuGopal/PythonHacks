#write code to add two  numbers

def add(a,b):
    return a+b

def test_add():
    assert add(2,3) == 5
    assert add('space','ship') == 'spaceship'


#write code to print fibonacci series till a given number

def fib(n):
    a,b = 0,1
    while a<n:
        print(a, end=' ')
        a,b = b, a+b
    print()

def test_fib():
    assert fib(10) == 0,1,1,2,3,5,8
    assert fib(100) == 0,1,1,2,3,5,8,13,21,34,55,89
