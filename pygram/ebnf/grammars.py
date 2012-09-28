"""
Yo dawg, I heard you like creating grammars, so we create a EBNF grammar
so you can create grammar while you create grammar
"""


from ..core.reductions import Reduction
from ..grammars.cfg import CFGExtended, CFGRule
from .symbols import t, nt

#TODO: grammar

R = CFGRule


def identity(x):
    return x


def handle_spec(rule_list):
    return rule_list


def handle_rule_list_1(rule_list, semicolon, rule):
    assert(semicolon == ';')
    return rule_list + (rule,)


def handle_rule_list_2(rule):
    return (rule,)


def handle_rule(head, eq, body):
    assert(eq == '=')
    return (head, body)


reductions = [

    Reduction(R(nt.specification, (nt.rule_list,)), handle_spec),

    Reduction(R(nt.rule_list, (nt.rule_list, t.SEMICOLON, nt.rule)), handle_rule_list_1),
    Reduction(R(nt.rule_list, (nt.rule,)), handle_rule_list_2),

    Reduction(R(nt.rule, (nt.head, t.EQUALS, nt.body)), handle_rule),

    Reduction(R(nt.head, (t.IDENT,)), identity),

    Reduction(R(nt.body, (nt.exp,)), identity),

    Reduction(R(nt.body, (nt.e,)), identity),
]
