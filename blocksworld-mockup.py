
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

    # predicates

    # type annotation styles. these are not good because we can't specify the parameter names.
    # Wrapping them will end up being redundant.
    clear:    Callable[[Object], bool]
    on_table: Callable[[Object], bool]
    on:       Callable[[Object, Object], bool]

    clear:    Predicate[Object]
    on_table: Predicate[Object]
    on:       Predicate[Object, Object]

    # redundant
    clear:    Predicate[Object("x")]
    on_table: Predicate[Object("x")]
    on:       Predicate[Object("x"), Object("y")]

    clear:    Predicate[1]
    on_table: Predicate[1]
    on:       Predicate[2]

    # class attribute style

    # redundant
    clear     = Predicate("x")
    on_table  = Predicate("x")
    on        = Predicate("x","y")

    # Sexp style
    predicates = [
        ["clear", "x"],
        ["on_table", "x"],
        ["on", "x", "y"]
    ]

    # decorator style. See: inspect.signature(fn).parameters
    @predicate
    def clear(x):
        pass
    @predicate
    def on_table(x):
        pass
    @predicate
    def on(x, y):
        pass

    # constants
    table : Object
    
    table = Object()

    objects = ["table"]

    # actions
    # type declaration style --- same as predicates, not informative when producing pddls
    move_b_to_b: Callable[[Object, Object, Object], Action]

    # declrator style
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


