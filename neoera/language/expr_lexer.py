import re


class ExprToken:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __repr__(self):
        return f"ExprToken({self.kind}, {self.value})"


class ExprLexer:
    KEYWORDS = {"and", "or", "not", "in"}

    TOKEN_REGEX = re.compile(
        r"""
        (?P<SPACE>\s+)                               |
        (?P<NUMBER>\d+(\.\d+)?)                       |
        (?P<STRING>"[^"]*"|'[^']*')                   |
        (?P<OP>==|!=|>=|<=|[+\-*/<>])                 |
        (?P<EQUAL>=)                                  |
        (?P<LBRACK>\[)                                |
        (?P<RBRACK>\])                                |
        (?P<LPAREN>\()                                |
        (?P<RPAREN>\))                                |
        (?P<COMMA>,)                                  |
        (?P<COLON>:)                                  |
        (?P<WORD>[\w\u4e00-\u9fa5]+)
        """,
        re.VERBOSE
    )

    def tokenize_expr(self, text):
        tokens = []
        pos = 0

        while pos < len(text):
            m = self.TOKEN_REGEX.match(text, pos)
            if not m:
                raise SyntaxError(f"Unrecognized char: {text[pos]} at {pos}")

            kind = m.lastgroup
            value = m.group(kind)
            pos = m.end()

            if kind == "SPACE":
                continue

            if kind == "NUMBER":
                value = float(value) if "." in value else int(value)
                tokens.append(ExprToken("NUMBER", value))
            elif kind == "STRING":
                tokens.append(ExprToken("STRING", value[1:-1]))
            elif kind == "WORD":
                v2 = value.lower()
                if v2 in self.KEYWORDS:
                    tokens.append(ExprToken("KEYWORD", v2))
                else:
                    tokens.append(ExprToken("IDENT", value))
            else:
                tokens.append(ExprToken(kind, value))

        return tokens
