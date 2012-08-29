from ...core.symbols import SymbolSet
from ...core.reductions import Reduction
from ...grammars.cfg import CFGExtended, CFGRule

R = CFGRule

t = SymbolSet('t', (
    ('NEWLINE', '\n'),
    'INDENT',
    'DEDENT',
    ('SEMICOLON', ';'),
    ('COLON', ','),
    ('PERIOD', '.'),
))

nt = SymbolSet('nt', (
    'compound_stmt',
    'stmt_list',
    'statement',
    'suite',
    'suite_core',
    'simple_stmt',
))

identity = lambda x: x

reductions = [
    Reduction(R(nt.stmt_list, (nt.simple_stmt,)), lambda x: (x,)),
    Reduction(R(nt.stmt_list, (nt.stmt_list, t.SEMICOLON, nt.simple_stmt)), lambda x1, _, x2: x1 + (x2,)),

    Reduction(R(nt.statement, (nt.stmt_list, t.NEWLINE)), lambda x1, _: x1),
    Reduction(R(nt.statement, (nt.stmt_list, t.SEMICOLON, t.NEWLINE)), lambda x, _, __: x),
    Reduction(R(nt.statement, (nt.compound_stmt,)), lambda x: (x,)),

    Reduction(R(nt.suite_core, (t.statement)), lambda x: x),
    Reduction(R(nt.suite_core, (nt.suite_core, t.statement)), lambda x1, x2: x1 + x2),

    Reduction(R(nt.suite, (t.NEWLINE, t.INDENT, nt.suite_core, t.DEDENT)), lambda _, __, x, ___: x),
    Reduction(R(nt.suite, (nt.stmt_list, t.NEWLINE)), lambda x, _: x),
    Reduction(R(nt.suite, (nt.stmt_list, t.SEMICOLON, t.NEWLINE)), lambda x, _, __: x),
]

'''
compound_stmt ::=  if_stmt
                   | while_stmt
                   | for_stmt
                   | try_stmt
                   | with_stmt
                   | funcdef
                   | classdef
                   | decorated
suite         ::=  stmt_list NEWLINE | NEWLINE INDENT statement+ DEDENT
statement     ::=  stmt_list NEWLINE | compound_stmt
stmt_list     ::=  simple_stmt (";" simple_stmt)* [";"]
'''
