

class A:
    a : str
    b : int

print(A.__dict__)
print(A().__dict__)

A.a = "a"

print(A.__dict__)
print(A().__dict__)
print(A.a)

A.a = 1

print(A.__dict__)
print(A().__dict__)
print(A.a)
print(A().a)
print(A.b)
