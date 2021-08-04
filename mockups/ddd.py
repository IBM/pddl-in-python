import re

# doesnt work

# def fn():
#     clear(x)
# 
# 
# def eval_with_fix(f):
#     try:
#         f()
#     except NameError as e:
#         print(e)
#         name = re.findall("name '(\w+)' is not defined",str(e))[0]
#         print(name)
# 
#         fail = True
#         args = []
#         while fail:
#             argstring = ','.join(args)
#             print(f"def {name}({argstring}): pass")
#             print(exec(f"def {name}({argstring}): pass",globals()))
#             try:
#                 f()
#                 fail = False
#             except NameError as e:
#                 print(e)
#                 argname = re.findall("name '(\w+)' is not defined",str(e))[0]
#                 print(argname)
#                 args.extend(argname)
#     return
# 
# eval_with_fix(fn)

def fn():
    clear("x")


def eval_with_fix(f):
    fail = True
    f.undefined = {}
    while fail:
        try:
            f()
            fail = False
        except NameError as e:
            print(e)
            name = re.findall("name '(\w+)' is not defined",str(e))[0]
            print(name)
            
            body = f"def {name}(*args): {f.__name__}.undefined['{name}'] = args"
            print(body)
            print(exec(body,globals()))
    return

eval_with_fix(fn)
print(vars(fn))
