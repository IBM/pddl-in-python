
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





class Domain:
    def __getattr__(self, method_name):
        predicate = lambda *args: pass
        predicate.__name__ = method_name
        self.predicates.extend(predicate)
        setattr(self, method_name, predicate)
        return predicate

@domain
class Blocksworld(Domain):
    def move_b_to_b(bm, bf, bt):
        if self.clear(bm) and self.clear(bt) and self.on(bm, bf):
            self.clear(bt)  = False
            self.on(bm, bf) = False
            self.on(bm, bt) = True
            self.clear(bf)  = True

    def move_b_to_t(bm, bf):
        if self.clear(bm) and self.on(bm, bf):
            self.on(bm, bf)   = False
            self.on_table(bm) = True
            self.clear(bf)    = True

    def move_t_to_b(bm, bt):
        if self.clear(bm) and self.clear(bt) and self.on_table(bm):
            self.clear(bt)    = False
            self.on_table(bm) = False
            self.on(bm, bt)   = True
