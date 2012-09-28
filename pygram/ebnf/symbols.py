from ..core.symbols import SymbolSet

t = SymbolSet('t', (
    'IDENT',
    'STRING',
    'REGEXP',
    ('EQUALS', '='),
    ('SEMICOLON', ';'),
    ('COMMA', ','),
    ('PERIOD', '.'),
    ('PLUS', '+'),
    ('STAR', '*'),
    ('RBRA_O', '('),
    ('RBRA_C', ')'),
    ('SBRA_O', '['),
    ('SBRA_C', ']'),
    ('CBRA_O', '{'),
    ('CBRA_C', '}'),
))

nt = SymbolSet('nt', (
    'specification',
    'rule_list',
    'rule',
    'head',
    'body',
    'exp',
    'alternative_list',
    'alternative',
    'atom',
))
