def decorator(func):
    
    def wrapper(*args):
        print("I am a wrapper")
        print(*args)
        return func(*args)
    
    return wrapper

# old fashioned representation

'''
def function1(*arg1):
    print("I am actual function")
    print(*arg1)

f1 = decorator(function1)

f1(1,2)
'''

# syntactic sugar

@decorator
def function1(*arg1):
    print("I am actual function")
    print(*arg1)

function1(1,3)


# syntactic sugar explanation

'''
def function1(*args):
    print("I am actual function")
    print(*args)

decorator(function1)(1,3)
'''
