"""A Pygments lexer for NiteCode language."""
from pygments.lexer import RegexLexer, words, bygroups, include, using, this, inherit
from pygments.token import *
from pygments import unistring as uni

__all__ = ("NiteCodeLexer",)


class NiteCodeLexer(RegexLexer):
    name = 'NiteCode'
    aliases = ['nite', 'nitecode']
    filenames = ['*.nite', '*.nitecode']
    mimetypes = ['text/x-nitecode']

    nite_identifier = (r'[_' + uni.combine('Lu', 'Ll', 'Lm', 'Lt', 'Nl') + r']' # Begin character
                       r'[_' + uni.combine('Lu', 'Ll', 'Lm', 'Lt', 'Nl', 'Nd', 'Pc', 'Cf', 'Mn', 'Mc') + r']*')

    tokens = {
        'root': [
            include('comments'),
            include('numbers_int'),
            include('numbers_float'),
            include('builtin_types'),

            (r'(use|module)', Keyword, 'module_path'), # use, module

            (r'(' + nite_identifier + r')' + # Function name
             r'(\s*)(\()', # Punctuation
             bygroups(Name.Function, Whitespace, Punctuation)), # Functions

            (r'(enum)?(\s*)' # enum keyword
             r'(type)(\s*)' # type keyword
             r'(' + nite_identifier + r')', # Type name
             bygroups(Keyword, Whitespace, Keyword, Whitespace, Name.Class)),

            (words((
                '>>>=', '>>=', '<<=', '<=', '>=', '+=', '-=', '*=', '/=',
                '%=', '&=', '|=', '^=', '??=', '??', '?.', '!=', '==',
                '&&', '||', '>>>', '>>', '<<', '++', '--', '+', '-', '*',
                '/', '%', '&', '|', '^', '<', '>', '?', '!', '~', '=',
             )), Operator),
            (r'=~|!=|==|<<|>>|[-+/*%=<>&^|]', Operator),
            (r'[;{}()\[\],\.]', Punctuation), # Punctuation
            (r'"', String, 'string_content'),
            (r"'\\.'|'[^\\]'", String.Char), # Char

            include('keywords'),

            (nite_identifier, Name),
        ],
        'keywords': [
            (words((
                'if', 'else',
                'loop', 'for', 'do', 'while',
                'typeof', 'sizeof', 'offsetof', 'default'
                'break', 'return', 'continue',
                'where', 'is', 'as',
                'const',
                'public', 'friend', 'protected', 'internal', 'family', 'private',
                'nogeneric', 'virtual', 'static', 'volatile',
                'new', 'get', 'set',
                'operator', 'implicit', 'explicit', 'commutative',
            )), Keyword),
            (words((
                'false', 'true', 'nil',
            )), Keyword.Constant)
        ],
        'comments': [
            (r'\/\/.*?\n', Comment.Single),
            (r'(?s)\/\*.*?\*\/', Comment.Multiline),
        ],
        "builtin_types": [
            (r'u8|u16|u32|u64|i8|i16|i32|i64|f32|f64|bool|void\b', Keyword.Type)
        ],
        'numbers_int': [
            (r'0x[0-9a-fA-F]+([ui]((8)|(16)|(32)|(64))?)?', Number.Hex),
            (r'0b[01]+([ui]((8)|(16)|(32)|(64))?)?', Number.Bin),
            (r'[0-9]+([ui]((8)|(16)|(32)|(64))?)?', Number.Integer),
        ],
        'numbers_float': [
            (r'([0-9]+(f((32)|(64))?)?)', Number.Float),
        ],
        'module_path': [
            (r'(\s*)\(', Punctuation, '#pop'), # use(x ...) {}
            (r'(\s*)(' + nite_identifier + r')', bygroups(Whitespace, Name.Namespace), 'module_path_continue'),
            (r'', Name.Namespace, '#pop'), # Fallback
        ],
        'module_path_continue': [
            (r'(\s*)(::)(\s*)(' + nite_identifier + r')', bygroups(Whitespace, Punctuation, Whitespace, Name.Namespace)),
            (r'(\s*)(as)(\s*)(' + nite_identifier + r')', bygroups(Whitespace, Keyword, Whitespace, Name.Namespace), '#pop'), # use XYW as XYZ
            (r'', Name.Namespace, '#pop'), # Fallback
        ],
        'string_content': [
            (r'([^\\])(\$\{)(.*)(\})', bygroups(String, String.Interpol, using(this), String.Interpol)),
            (r'[^\\]"', String, '#pop'),
            (r'.', String),
        ]
    }