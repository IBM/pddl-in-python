
class Variable:
    pass

class Predicate:
    pass

class Condition:
    pass


def predicate(fn):
    pass
def preconditions(fn):
    pass
def effects(fn):
    pass
def domain(fn):
    pass





@domain
class Blocksworld:

    @predicate
    def clear(x):
        pass
    @predicate
    def on_table(x):
        pass
    @predicate
    def on(x, y):
        pass

    table : Object
    
    @preconditions
    def move_b_to_b(bm, bf, bt):
        return clear(bm) and clear(bt) and on(bm, bf)
    @effects
    def move_b_to_b(bm, bf, bt):
        return not clear(bt) and not on(bm, bf) and on(bm, bt) and clear(bf)

    @preconditions
    def move_b_to_t(bm, bf):
        return clear(bm) and on(bm, bf)
    @effects
    def move_b_to_t(bm, bf):
        return not on(bm, bf) and on_table(bm) and clear(bf)

    @preconditions
    def move_t_to_b(bm, bt):
        return clear(bm) and clear(bt) and on_table(bm)
    @effects
    def move_t_to_b(bm, bt):
        return not clear(bt) and not on_table(bm) and on(bm, bt)


