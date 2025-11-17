# neoera/language/expr_lexer.py

import re


class ExprToken:
    def __init__(self, type_, value, pos):
        self.type = type_
        self.value = value
        self.pos = pos

    def __repr__(self):
        return f"ExprToken({self.type}, {self.value})"


class ExprLexer:
    """
    NSL 表达式词法分析器（Tokenizer）
    支持：
    - 数字：123, 1.5
    - 字符串："abc" 'abc'
    - 标识符：变量、函数（支持中文）
    - 操作符：== != >= <= && || + - * / ! in not
    - 括号：() []
    - 逗号
    """

    # 操作符优先级决定解析顺序
    OPERATORS = {
        "==", "!=", ">=", "<=", ">", "<",
        "+", "-", "*", "/", "!", "&&", "||",
    }

    KEYWORDS = {"true", "false", "not", "and", "or", "in"}

    TOKEN_REGEX = re.compile(
        r"""
        (?P<SPACE>\s+)                               | 
        (?P<NUMBER>\d+(\.\d+)?)                       |
        (?P<STRING>"[^"]*"|'[^']*')                   |
        (?P<OPERATOR>==|!=|>=|<=|\|\||&&|[+\-*/!<>])  |
        (?P<COMMA>,)                                  |
        (?P<LBRACK>\[)                                |
        (?P<RBRACK>\])                                |
        (?P<LPAREN>\()                                |
        (?P<RPAREN>\))                                |
        (?P<WORD>[\w\u4e00-\u9fa5]+)                  # 支持中文变量名
        """,
        re.VERBOSE
    )

    def tokenize(self, text):
        tokens = []
        pos = 0
        length = len(text)

        while pos < length:
            match = self.TOKEN_REGEX.match(text, pos)
            if not match:
                raise SyntaxError(f"[ExprLexer] 无法解析的字符: {text[pos]} at {pos}")

            kind = match.lastgroup
            value = match.group(kind)
            pos = match.end()

            if kind == "SPACE":
                continue

            elif kind == "NUMBER":
                tokens.append(ExprToken("NUMBER", float(value) if "." in value else int(value), pos))

            elif kind == "STRING":
                tokens.append(ExprToken("STRING", value[1:-1], pos))

            elif kind == "WORD":
                lower = value.lower()
                if lower in self.KEYWORDS:
                    tokens.append(ExprToken("KEYWORD", lower, pos))
                else:
                    tokens.append(ExprToken("IDENT", value, pos))

            elif kind == "OPERATOR":
                tokens.append(ExprToken("OP", value, pos))

            elif kind == "COMMA":
                tokens.append(ExprToken("COMMA", value, pos))

            elif kind == "LBRACK":
                tokens.append(ExprToken("LBRACK", value, pos))

            elif kind == "RBRACK":
                tokens.append(ExprToken("RBRACK", value, pos))

            elif kind == "LPAREN":
                tokens.append(ExprToken("LPAREN", value, pos))

            elif kind == "RPAREN":
                tokens.append(ExprToken("RPAREN", value, pos))

        return tokens
