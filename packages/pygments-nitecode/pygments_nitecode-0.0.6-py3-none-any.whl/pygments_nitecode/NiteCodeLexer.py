"""A Pygments lexer for NiteCode language."""
from pygments.lexer import RegexLexer, words, bygroups, include
from pygments.token import *

__all__ = ("NiteCodeLexer",)


class NiteCodeLexer(RegexLexer):
    name = 'NiteCode'
    aliases = ['nite', 'nitecode']
    filenames = ['*.nite', '*.nitecode']
    mimetypes = ['text/nitecode']

    tokens = {
        'root': [
            (r'\/\/.*?\n', Comment.Single),
            (r'(?s)\/\*.*?\*\/', Comment.Multiline),
            (r'0x[0-9a-fA-F]+([ui]((8)|(16)|(32)|(64)))?', Number.Hex),
            (r'[0-9]+([ui]((8)|(16)|(32)|(64)))?', Number.Integer),
            (r'0b[01]+([ui]((8)|(16)|(32)|(64)))?', Number.Bin),
            (r'[%+\-~=^|&<>!&?:\/*]', Operator),
            (r'[;{}()\[\],\.]', Punctuation),
            (r'\'([^\']|\\[abefnrtv\\\'\"]|\\u[0-9a-fA-F]+)\'', String.Char),
            (words((
                'u8', 'u16', 'u32', 'u64',
                'i8', 'i16', 'i32', 'i64',
                'f32', 'f64',
                'void'
            ), suffix=r'\b'), Keyword.Type),
            (words((
                'use',
                'type', 'enum',
                'if', 'else',
                'while', 'do', 'loop', 'for'
                'break', 'continue', 'return'
            ), suffix=r'\b'), Keyword),
            (words((
                'true', 'false', 'nil'
            ), suffix=r'\b'), Keyword.Constant),
            (r'[a-zA-Z_]\w*', Name),
        ]
    }