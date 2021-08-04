import stacktrace
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
    def __str__(self):
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
    args : list[str]
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
            s += textwrap.indent(f"\n{c}","    ")
        s += ")"
        return s
@dataclass
class Or(Condition):
    conditions : list[Condition]
    def __str__(self):
        s = f"(or"
        for c in self.conditions:
            s += textwrap.indent(f"\n{c}","    ")
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
        s += textwrap.indent(f"{self.body}","    ")
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
            s += textwrap.indent(f"\n:preconditions\n{self.preconditions}","    ")
        if self.effects:
            s += textwrap.indent(f"\n:effects\n{self.effects}","    ")
        s += ")"
        return s


class Domain:
    def __init__(self):
        self.__actions__ = {}
        for name in dir(self):
            method = getattr(self,name)
            if name[0] != "_" and callable(method):
                self.__actions__[name] = self.__parse(method)

    def __parse(self,action):
        action = ast.parse(textwrap.dedent(inspect.getsource(action))).body[0]
        name = action.name
        args = [Variable(arg.arg) for arg in action.args.args]

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
                results = [ parse_predicate(elem) for elem in stmt.values]
                if isinstance(stmt.op,ast.And):
                    return And(results)
                elif isinstance(stmt.op,ast.Or):
                    return Or(results)
                else:
                    assert False, f"unsupported op: {stmt.op} in {ast.unparse(stmt)}"
            elif isinstance(stmt,ast.UnaryOp):
                assert isinstance(stmt.op, ast.Not)
                return ~ parse_predicate(stmt.operand)
            else:
                assert False, f"unsupported op: {stmt.op} in {ast.unparse(stmt)}"

        def parse_effects(body):
            return And([ parse_effect(stmt) for stmt in body ])

        def parse_effect(stmt):
            if isinstance(stmt,ast.If):
                return parse_conditional_effect(stmt)
            elif isinstance(stmt,ast.Assign):
                results = []
                for target, value in zip(stmt.targets, maybe_iter_tuple(stmt.value)):
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
            return Predicate(name, args)

        def parse_arg(arg):
            if isinstance(arg,ast.Constant):
                return Variable(arg.value)
            if isinstance(arg,ast.Name):
                return Variable(arg.id)
            assert False
            

        return parse_toplevel(action.body)

    def __str__(self):
        s = f"(domain {self.__class__.__name__.lower()}"
        s += textwrap.indent(f"\n(:requirement :strips)","    ")
        for action in self.__actions__.values():
            s += textwrap.indent(f"\n{action}","    ")
        s += ")"
        return s

