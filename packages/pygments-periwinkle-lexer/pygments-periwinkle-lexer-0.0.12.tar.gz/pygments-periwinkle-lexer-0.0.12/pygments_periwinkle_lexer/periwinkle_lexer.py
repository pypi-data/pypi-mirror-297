import re

from pygments.lexer import RegexLexer, bygroups
from pygments.token import (
    Comment,
    Name,
    Keyword,
    Text,
    Punctuation,
    Operator,
    String,
    Number,
)


class PeriwinkleLexer(RegexLexer):
    name = 'Periwinkle'
    aliases = ['periwinkle']
    filenames = ['*.бр', '.барвінок']
    flags = re.UNICODE

    tokens = {
        'root': [
            (r'\A#!.*', Comment.Hashbang),
            (r'!.*', Comment),
            (r'\b(друк|друкр|зчитати|ітератор|Число|Логічний|Стрічка|Дійсний|Список|КінецьІтерації)\b', Name.Builtin),
            (r"(\bфункція\b)(\s*)([а-щА-ЩьюяїієґЬЮЯЇІЄҐ_][а-щА-ЩьюяїієґЬЮЯЇІЄҐ0-9_']*)(?=\s*\()",
             bygroups(Keyword.Control, Text.Whitespace, Name.Function)),
            (r',|[.]{3}', Punctuation),
            (r"[а-щА-ЩьюяїієґЬЮЯЇІЄҐ_][а-щА-ЩьюяїієґЬЮЯЇІЄҐ0-9_']*(?=\s*\()", Name.Function),
            (r'\b(якщо|або|інакше|кінець|поки|пропустити|завершити|повернути|обійти|спробувати|обробити|як|наприкінці|жбурнути)\b', Keyword),
            (r'(\b(не рівно|рівно|не є|не|та|або|більше рівно|більше|менше рівно|менше|є)\b)', Keyword.Operator),
            (r'=|\+=|-=|\*=|/=|//=|%=|\+|-|\*|/|//|%|\(|\)', Operator),
            (r'"', String, 'string'),
            (r'(([0-9]+[.][0-9]*)|([0-9]*[.][0-9]+))', Number.Float),
            (r'(0|([1-9][0-9]*))', Number.Integer),
            (r'\b(істина|хиба|ніц)\b', Name.Constant),
            (r"[а-щА-ЩьюяїієґЬЮЯЇІЄҐ_][а-щА-ЩьюяїієґЬЮЯЇІЄҐ0-9_']*", Name),
            (r'\s+', Text.Whitespace),
        ],
        'string': [
            (r'\\.', String.Escape),
            (r'[^*"]', String),
            (r'"', String, '#pop'),
        ],
    }
