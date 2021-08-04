
@dataclass
class Variable:
    name : str

class Condition:
    def __and__(a, b):
        return And(a, b)
    def __or__(a, b):
        return Or(a, b)
    def __not__(a):
        return Not(a, b)

@dataclass
class Predicate(Condition):
    name : str
    args : list[str]
@dataclass
class And(Condition):
    a : Any
    b : Any
@dataclass
class Or(Condition):
    a : Any
    b : Any
@dataclass
class Not(Condition):
    a : Any




def domain(cls):
    actions = vars(cls)
    cls.predicates = {}
    for name, definition in actions.items():
        fail = True
        params = inspect.signature(definition).parameters.keys()
        while fail:
            try:
                definition(params)
                fail = False
            except NameError as e:
                print(e)
                name = re.findall("name '(\w+)' is not defined",str(e))[0]
                print(name)

                predicate = lambda *args: pass
                predicate.__name__ = name
                setattr(cls, name, predicate)
    return


@domain
class Blocksworld:

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


