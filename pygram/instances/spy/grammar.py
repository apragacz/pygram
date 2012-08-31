from ...core.symbols import SymbolSet
from ...core.reductions import Reduction
from ...grammars.cfg import CFGExtended, CFGRule
from .statements import IfElseStatement

R = CFGRule

t = SymbolSet('t', (
    ('NEWLINE', '\n'),
    'INDENT',
    'DEDENT',
    ('SEMICOLON', ';'),
    ('COLON', ':'),
    ('COMMA', ','),
    ('PERIOD', '.'),
    ('IF', 'if'),
    ('ELSE', 'else'),
    ('ELIF', 'elif'),
))

nt = SymbolSet('nt', (
    'expression',

    'if_stmt',
    'while_stmt',
    'for_stmt',
    'try_stmt',
    'with_stmt',
    'funcdef',
    'classdef',
    'decorated',

    'compound_stmt',
    'stmt_list',
    'statement',
    'suite',
    'suite_core',
    'simple_stmt',
))

identity = lambda x: x

reductions = [

#if_stmt ::=  "if" expression ":" suite
#             ( "elif" expression ":" suite )*
#             ["else" ":" suite]
    Reduction(R(nt.if_stmt, (t.IF, nt.expression, t.COLON, nt.suite, t.ELSE, t.COLON, nt.suite)), lambda _, e1, __, sl1, ___, ____, s2: IfElseStatement((e1, sl1), s2)),

    Reduction(R(nt.compound_stmt, (nt.if_stmt,)), identity),
    Reduction(R(nt.compound_stmt, (nt.if_stmt,)), identity),

    Reduction(R(nt.stmt_list, (nt.simple_stmt,)), lambda s: (s,)),
    Reduction(R(nt.stmt_list, (nt.stmt_list, t.SEMICOLON, nt.simple_stmt)), lambda sl, _, s: sl + (s,)),

    Reduction(R(nt.statement, (nt.stmt_list, t.NEWLINE)), lambda sl, _: sl),
    Reduction(R(nt.statement, (nt.stmt_list, t.SEMICOLON, t.NEWLINE)), lambda sl, _, __: sl),
    Reduction(R(nt.statement, (nt.compound_stmt,)), lambda s: (s,)),

    Reduction(R(nt.suite_core, (t.statement)), identity),
    Reduction(R(nt.suite_core, (nt.suite_core, t.statement)), lambda x1, x2: x1 + x2),

    Reduction(R(nt.suite, (t.NEWLINE, t.INDENT, nt.suite_core, t.DEDENT)), lambda _, __, x, ___: x),
    Reduction(R(nt.suite, (nt.stmt_list, t.NEWLINE)), lambda x, _: x),
    Reduction(R(nt.suite, (nt.stmt_list, t.SEMICOLON, t.NEWLINE)), lambda x, _, __: x),
]
