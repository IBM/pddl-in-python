from . import stacktrace
import warnings
import ast
import textwrap
import functools
import inspect
from dataclasses import dataclass
from typing import Optional

@dataclass
class Variable:
    name : str
    type : Optional[str] = None
    def __str__(self):
        if self.type:
            return f"?{self.name} - {self.type}"
        else:
            return f"?{self.name}"

@dataclass
class Condition:
    def __and__(a, b):
        return And([a, b])
    def __or__(a, b):
        return Or([a, b])
    def __invert__(a):
        return Not(a)

@dataclass
class Predicate(Condition):
    name : str
    args : list[Variable]
    def __str__(self):
        s = f"({self.name}"
        for arg in self.args:
            s += f" {arg}"
        s += ")"
        return s
        
@dataclass
class And(Condition):
    conditions : list[Condition]
    def __str__(self):
        s = f"(and"
        for c in self.conditions:
            s += textwrap.indent(f"\n{c}","  ")
        s += ")"
        return s
@dataclass
class Or(Condition):
    conditions : list[Condition]
    def __str__(self):
        s = f"(or"
        for c in self.conditions:
            s += textwrap.indent(f"\n{c}","  ")
        s += ")"
        return s
@dataclass
class Not(Condition):
    a : Condition
    def __str__(self):
        s = f"(not {self.a})"
        return s
@dataclass
class When(Condition):
    test : Condition
    body : Condition
    def __str__(self):
        s = f"(when {self.test}"
        s += textwrap.indent(f"\n{self.body}","  ")
        s += ")"
        return s


@dataclass
class Action:
    name: str
    params: list[str]
    preconditions : Optional[Condition]
    effects : Optional[Condition]
    def __str__(self):
        s = ""
        s += f"(:action {self.name} :parameters ("
        first = True
        for p in self.params:
            if not first:
                s += f" "
            s += f"{p}"
            first = False
        s += f")"
        if self.preconditions:
            s += textwrap.indent(f"\n:preconditions\n{self.preconditions}"," ")
        if self.effects:
            s += textwrap.indent(f"\n:effects\n{self.effects}"," ")
        s += ")"
        return s


# Note: All methods must begin with __ .
# Otherwise, the method itself is recognized as an action by the parser.

class Domain:
    def __init__(self):
        self.__actions__ = {}
        self.__predicates__ = {}
        for name in dir(self):
            method = getattr(self,name)
            if name[0] != "_" and callable(method):
                self.__actions__[name] = self.__parse(method)

    def __parse(self,action):
        action = ast.parse(textwrap.dedent(inspect.getsource(action))).body[0]
        name = action.name
        args = [Variable(arg.arg,arg.annotation.id) if arg.annotation else Variable(arg.arg, None)
                for arg in action.args.args]

        def parse_toplevel(body):
            if isinstance(body[0],ast.If):
                if len(body) > 1:
                    # it has several conditional effects
                    return Action(name, args, None, parse_effects(body))
                else:
                    # it has preconditions
                    return Action(name, args, *parse_precondition(body[0]))
            elif isinstance(body[0],ast.Assign):
                # no precondition
                return Action(name, args, None, parse_effects(body))
            else:
                assert False, f"invalid body in {ast.unparse(action)}: should start from If or Assign AST"

        def parse_precondition(stmt):
            assert isinstance(stmt,ast.If)
            return parse_condition(stmt.test), parse_effects(stmt.body)

        def parse_conditional_effect(stmt):
            assert isinstance(stmt,ast.If)
            return When(
                parse_condition(stmt.test),
                parse_effects(stmt.body))

        def parse_condition(stmt):
            if isinstance(stmt,ast.BoolOp):
                results = [ parse_condition(elem) for elem in stmt.values]
                if isinstance(stmt.op,ast.And):
                    return And(results)
                elif isinstance(stmt.op,ast.Or):
                    return Or(results)
                else:
                    assert False, f"unsupported op: {ast.unparse(stmt)}"
            elif isinstance(stmt,ast.UnaryOp):
                assert isinstance(stmt.op, ast.Not)
                return ~ parse_predicate(stmt.operand)
            elif isinstance(stmt,ast.Subscript):
                return parse_predicate(stmt)
            else:
                assert False, f"unsupported op: {ast.unparse(stmt)}"

        def parse_effects(body):
            return And([ parse_effect(stmt) for stmt in body ])

        def parse_effect(stmt):
            if isinstance(stmt,ast.If):
                return parse_conditional_effect(stmt)
            elif isinstance(stmt,ast.Assign):
                # allows tuple-type insertion too
                assert len(stmt.targets) == 1
                results = []
                for target, value in zip(maybe_iter_tuple(stmt.targets[0]), maybe_iter_tuple(stmt.value)):
                    if value.value:
                        results.append(parse_predicate(target))
                    else:
                        results.append(~parse_predicate(target))
                if len(results) > 1:
                    return And(results)
                else:
                    return results[0]
            else:
                assert False, f"unsupported statement in {ast.unparse(stmt)}"

        def maybe_iter_tuple(node):
            if isinstance(node, ast.Tuple):
                for elt in node.elts:
                    yield elt
            else:
                yield node

        def parse_predicate(predicate):
            assert isinstance(predicate,ast.Subscript)
            assert isinstance(predicate.value,ast.Name)
            name = predicate.value.id
            args = [ parse_arg(elt) for elt in maybe_iter_tuple(predicate.slice) ]
            if name not in self.__predicates__:
                self.__predicates__[name] = Predicate(name, [ Variable(f"x{i}") for i, _ in enumerate(args)])
            return Predicate(name, args)

        def parse_arg(arg):
            if isinstance(arg,ast.Constant):
                return Variable(arg.value)
            if isinstance(arg,ast.Name):
                return Variable(arg.id)
            assert False
            
        try:
            return parse_toplevel(action.body)
        except:
            stacktrace.format()

    def __str__(self):
        try:
            return self.__str()
        except:
            stacktrace.format()

    def __str(self):
        s = f"(domain {self.__class__.__name__.lower()}"
        s += textwrap.indent(f"\n(:requirement :strips)","  ")
        s += textwrap.indent(f"\n(:predicates","  ")
        for predicate in self.__predicates__.values():
            s += textwrap.indent(f"\n{predicate}","    ")
        s += ")"
        for action in self.__actions__.values():
            s += textwrap.indent(f"\n{action}","  ")
        s += ")"
        return s

