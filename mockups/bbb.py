
def aaa(x):
    pass

print(aaa.__name__)
print(aaa.__dict__)
print(vars(aaa))

import inspect
print(inspect.signature(aaa).parameters)
