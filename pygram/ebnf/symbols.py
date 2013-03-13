from ..core.symbols import SymbolSet

t = SymbolSet('t', (
    'IDENT',
    'STRING',
    'SPECIAL',

    ('EQUALS', '='),
    ('SEMICOLON', ';'),
    ('COMMA', ','),
    ('OR', '|'),

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
    'concat_list',
    'concat',
    'atom',
))

token_config = (
    (t.IDENT, '_*[A-Za-z][A-Za-z0-9_ ]*'),
    (t.STRING, '"(\\"|[^"])*"'),
    (t.SPECIAL, '\\?[^\\?]*\\?'),

    (t.EQUALS, '='),
    (t.SEMICOLON, ';'),
    (t.COMMA, ','),
    (t.OR, '|'),

    (t.RBRA_O, '\\('),
    (t.RBRA_C, '\\)'),
    (t.SBRA_O, '\\['),
    (t.SBRA_C, '\\]'),
    (t.CBRA_O, '\\{'),
    (t.CBRA_C, '\\}'),
)
