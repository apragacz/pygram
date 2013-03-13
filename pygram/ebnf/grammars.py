"""
Yo dawg, I heard you like creating grammars, so we create a EBNF grammar
so you can create grammar while you create grammar
"""


from ..core.reductions import Reduction
from ..grammars.cfg import CFGExtended, CFGRule
from .symbols import t, nt
from .statements import (SpecificationStatement, RuleStatement,
                         AlternativeStatement, ConcatenationStatement,
                         RepetitionStatement, OptionStatement,
                         IdentStatement, StringStatement, SpecialStatement)

identity = lambda stmt: stmt
appended = lambda list_stmt, sep, stmt: list_stmt.appended(stmt)

'''
specification -> rule_list  # added

rule_list -> rule_list ; rule  # added
rule_list -> rule  # added

rule -> head = body  # added

head -> IDENT  # added

body -> exp  # added

exp -> atom
exp -> alternative_list

alternative_list -> alternative_list | alternative
alternative_list -> alternative

alternative -> concat_list

concat_list -> concat_list , concat
concat_list -> concat

concat -> atom

atom -> ( exp )  # added
atom -> { exp }  # added
atom -> [ exp ]  # added
atom -> IDENT  # added
atom -> STRING  # added
atom -> SPECIAL  # added
'''

reduction_spec = [
    # specification
    (nt.specification, [nt.rule_list], identity),

    # rule_list
    (nt.rule_list, [nt.rule_list, t.SEMICOLON, nt.rule], appended),
    (nt.rule_list, [nt.rule], SpecificationStatement),

    # rule
    (nt.rule, [nt.head, t.EQUALS, nt.body],
     lambda ident_stmt, _, exp_stmt: RuleStatement([ident_stmt, exp_stmt])),

    # head
    (nt.head, [t.IDENT], identity),

    # body
    (nt.body, [nt.exp], identity),

    # exp
    (nt.exp, [nt.atom], identity),
    (nt.exp, [nt.alternative_list], identity),

    # alternative_list
    (nt.alternative_list, [nt.alternative_list, t.OR, nt.alternative],
     appended)
    (nt.alternative_list, [nt.alternative], AlternativeStatement),

    # alternative
    (nt.alternative, [nt.concat_list], identity),

    # concat_list
    (nt.concat_list, [nt.concat_list, t.COMMA, nt.concat], appended)
    (nt.concat_list, [nt.concat], ConcatenationStatement),

    #concat
    (nt.concat, [nt.atom], identity),

    # atom
    (nt.atom, [t.RBRA_O, nt.exp, t.RBRA_C],
     lambda _, exp_stmt, __: exp_stmt),
    (nt.atom, [t.CBRA_0, nt.exp, t.CBRA_C],
     lambda _, exp_stmt, __: RepetitionStatement(exp_stmt)),
    (nt.atom, [t.SBRA_0, nt.exp, t.SBRA_C],
     lambda _, exp_stmt, __: OptionStatement(exp_stmt)),
    (nt.atom, [t.IDENT], IdentStatement),
    (nt.atom, [t.STRING], StringStatement),
    (nt.atom, [t.SPECIAL], SpecialStatement),
]

reductions = [Reduction(CFGRule(head, tuple(tail)), fun)
              for head, tail, fun in reduction_spec]
