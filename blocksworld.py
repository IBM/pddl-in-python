
from pypddl import Domain

class Blocksworld(Domain):
    def move_b_to_b(bm, bf, bt):
        if clear[bm] and clear[bt] and on[bm, bf]:
            clear[bt]  = False
            on[bm, bf] = False
            on[bm, bt] = True
            clear[bf]  = True

    def move_b_to_t(bm, bf):
        if clear[bm] and on[bm, bf]:
            on[bm, bf]   = False
            on_table[bm] = True
            clear[bf]    = True

    def move_t_to_b(bm, bt):
        if clear[bm] and clear[bt] and on_table[bm]:
            clear[bt]    = False
            on_table[bm] = False
            on[bm, bt]   = True

try:
    # print(And([Predicate("aaa",["b","c"]),Predicate("aaa",["b","c"])]))
    # print(Predicate("aaa",["b","c"]) & ~ Predicate("aaa",["b","c"]))
    print(Blocksworld())
except:
    stacktrace.format()

