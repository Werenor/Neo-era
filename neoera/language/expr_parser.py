# neoera/language/expr_parser.py
from neoera.language.expr_lexer import tokenize_expr


class ExprParser:
    """
    Pratt Parser for NSL Expressions
    Supports:
        literals, variables, (), unary ops,
        + - * /, comparisons, and/or,
        list literal, function call
    """

    def __init__(self):
        self.tokens = []
        self.pos = 0

        # 绑定前缀运算符
        self.prefix_parselets = {
            "NUMBER": self.parse_number,
            "STRING": self.parse_string,
            "IDENT": self.parse_ident,
            "(": self.parse_group,
            "[": self.parse_list,
            "-": self.parse_unary,
            "not": self.parse_unary,
            "!": self.parse_unary,
        }

        # 中缀（优先级从高到低）
        self.infix_parselets = {
            "*": (self.parse_binary, 50),
            "/": (self.parse_binary, 50),

            "+": (self.parse_binary, 40),
            "-": (self.parse_binary, 40),

            "==": (self.parse_binary, 30),
            "!="": (self.parse_binary, 30),
            "<":  (self.parse_binary, 30),
            "<="": (self.parse_binary, 30),
            ">":  (self.parse_binary, 30),
            ">="": (self.parse_binary, 30),

            "in": (self.parse_binary, 25),
            "not in": (self.parse_binary, 25),

            "and": (self.parse_binary, 20),
            "or": (self.parse_binary, 10),

            "(": (self.parse_call, 60),
        }

    # -------------------------
    # Token Controller
    # -------------------------
    def next(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def peek(self):
        return self.tokens[self.pos]

    def match(self, value):
        if self.peek().value == value:
            self.next()
            return True
        return False

    # -------------------------
    # Public API
    # -------------------------
    def parse(self, text):
        self.tokens = tokenize_expr(text)
        self.pos = 0
        expr = self.parse_expression(0)
        return expr

    # Pratt 核心
    def parse_expression(self, rbp):
        tok = self.next()

        # 前缀处理
        if tok.kind in self.prefix_parselets:
            left = self.prefix_parselets[tok.kind](tok)
        elif tok.value in self.prefix_parselets:
            left = self.prefix_parselets[tok.value](tok)
        else:
            raise SyntaxError(f"Unexpected token: {tok}")

        # 中缀处理
        while rbp < self.get_lbp():
            tok = self.next()

            if tok.value in self.infix_parselets:
                parselet, bp = self.infix_parselets[tok.value]
                left = parselet(left, tok, bp)
            else:
                raise SyntaxError(f"Unexpected infix: {tok}")

        return left

    def get_lbp(self):
        tok = self.peek()
        if tok.value in self.infix_parselets:
            return self.infix_parselets[tok.value][1]
        return 0

    # -------------------------
    # Prefix Parselets
    # -------------------------
    def parse_number(self, tok):
        return {"type": "number", "value": float(tok.value)}

    def parse_string(self, tok):
        return {"type": "string", "value": tok.value}

    def parse_ident(self, tok):
        return {"type": "var", "name": tok.value}

    def parse_group(self, tok):
        expr = self.parse_expression(0)
        self.match(")")
        return expr

    def parse_list(self, tok):
        items = []
        if not self.match("]"):
            while True:
                items.append(self.parse_expression(0))
                if self.match("]"):
                    break
                self.match(",")
        return {"type": "list", "items": items}

    def parse_unary(self, tok):
        rhs = self.parse_expression(100)
        return {"type": "unary", "op": tok.value, "rhs": rhs}

    # -------------------------
    # Infix Parselets
    # -------------------------
    def parse_binary(self, left, tok, bp):
        right = self.parse_expression(bp)
        return {"type": "binary", "op": tok.value, "left": left, "right": right}

    def parse_call(self, left, tok, bp):
        args = []
        if not self.match(")"):
            while True:
                args.append(self.parse_expression(0))
                if self.match(")"):
                    break
                self.match(",")
        return {"type": "call", "func": left, "args": args}
