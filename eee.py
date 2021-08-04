import textwrap
import inspect
import ast

def fn(x):
    return 1

print(ast.dump(ast.parse(inspect.getsource(fn))))

class A:
    def a(x):
        y[a], y[b] = True, False
        y = x[1]
        y[1] = x
        y["a"] = x
        y[1,x] = x
        y = True
        print(x)
        if x and not y:
            print(x)
        return 1

print(inspect.getsource(A.a))   # has an indent
print(ast.dump(ast.parse(inspect.getsource(A))))

parsed = ast.parse(textwrap.dedent(inspect.getsource(A.a)))
print(ast.dump(parsed))
print(parsed.body)
print(parsed.body[0])
print(parsed.body[0].name)
print(parsed.body[0].args.posonlyargs)
print(parsed.body[0].args.args)
print([arg.arg for arg in parsed.body[0].args.args])
print(parsed.body[0].body)
for body in parsed.body[0].body:
    print(ast.dump(body))


# fail
# def fn2(x):
#     unknownfn() = 1


# fail
def fn3(x):
    unknownfn[1] = 1

print(ast.dump(ast.parse(inspect.getsource(fn3))))
