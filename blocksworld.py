import functools
import inspect
from dataclasses import dataclass

@dataclass
class Variable:
    name : str


# in this method, there is no distinction between
# 
# if condition:
#     effect
#     if condition:
#         effect
# 
# if condition:
#     effect
# if condition:
#     effect


@dataclass
class Action:
    name: str
    params: list[str]
    model = []
    def register_condition(self, condition):
        if len(conditions) == 0:
            self.model.append(condition)
        else:
            c = conditions[-1]
            if isinstance(c,Condition) and isinstance(condition,Effect):
                conditions[-1].body = 

@dataclass
class Effect:
    condition : Condition
    value : bool

@dataclass
class Condition:
    domain : Any
    body = []
    def __and__(a, b):
        return And(a, b)
    def __or__(a, b):
        return Or(a, b)
    def __not__(a):
        return Not(a, b)
    def truth(self):
        # if truthness is asked, it means it is used as a condition
        self.domain.current_action.register_condition(self)
        return True

@dataclass
class Predicate(Condition):
    name : str
    args : list[str]
    def __getitem__(self,args):
        if hasattr(self,"args"):
            oldlen = len(self.args)
            newlen = len(args)
            assert oldlen == newlen, f"argument number mismatch for {self.name}: previously, {oldlen}; now, {newlen}"
        else:
            self.args = [ f"arg{i}" for i,_ in enumerate(args) ]

        return Predicate(self.name, args)

    def __setitem__(self,args,value):
        self.domain.current_action.register_effect(Effect(self,value))
        pass
        
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
        # called only when the method is missing
        predicate = Predicate(name=method_name,
                              domain=self)
        setattr(self, method_name, predicate)
        return predicate

    def __init__(self):
        self.actions   = {}
        self.predicate = {}
        for name, method in vars(self).items():
            params = list(inspect.signature(method).parameters.keys())
            action = Action(name,params)
            self.actions.append(action)
            self.current_action = action
            method(map(Variable, params))
        self.current_action = None
            

class Blocksworld(Domain):
    def move_b_to_b(self, bm, bf, bt):
        if self.clear[bm] and self.clear[bt] and self.on[bm, bf]:
            self.clear[bt]  = False
            self.on[bm, bf] = False
            self.on[bm, bt] = True
            self.clear[bf]  = True

    def move_b_to_t(self, bm, bf):
        if self.clear[bm] and self.on[bm, bf]:
            self.on[bm, bf]   = False
            self.on_table[bm] = True
            self.clear[bf]    = True

    def move_t_to_b(self, bm, bt):
        if self.clear[bm] and self.clear[bt] and self.on_table[bm]:
            self.clear[bt]    = False
            self.on_table[bm] = False
            self.on[bm, bt]   = True
