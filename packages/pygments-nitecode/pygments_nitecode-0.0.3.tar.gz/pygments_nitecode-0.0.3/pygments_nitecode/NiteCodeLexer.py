"""A Pygments lexer for NiteCode language."""
from pygments.lexer import RegexLexer, words, bygroups
from pygments.token import *

__all__ = ("NiteCodeLexer",)


class NiteCodeLexer(RegexLexer):
    name = 'NiteCode'
    aliases = ['nite', 'nitecode']
    filenames = ['*.nite', '*.nitecode']
    mimetypes = ['text/nitecode']

    tokens = {
        'root': [
            (r'\/\/.*$', Comment.Single),
            (r'0x[0-9a-fA-F]+([ui]((8)|(16)|(32)|(64)))?', Number.Hex),
            (r'[0-9]+([ui]((8)|(16)|(32)|(64)))?', Number.Integer),
            (r'[+-~=^|&<>!&?:\/*]', Operator),
            (r'[;{}()\[\],.]', Punctuation),
            (r'[a-zA-Z_]\w*', Name),
            # (r'(L?)(")', bygroups(String.Affix, String), 'string'),
            (words((
                # Types
                'u8', 'u16', 'u32', 'u64',
                'i8', 'i16', 'i32', 'i64',
                'f32', 'f64',
                'void',
                # Flow keywords
                'for', 'do', 'while',
                'if', 'else',
                'return',
                # Other
                'use', 'type'
            )), Keyword),
            (words((
                # Constants
                'false', 'true', 'nil'
            )), Keyword.Constant),
        ]
    }