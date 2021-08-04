
"""moduledoc"""
print(locals())
print(globals())


class A:
    """classdoc"""
    print("hi")
    print(A)
    print(locals())
    print(globals())
    pass

print(A())
