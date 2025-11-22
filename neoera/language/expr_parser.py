from neoera.language.expr_lexer import ExprLexer
from neoera.language.expr_lexer import ExprToken


class ExprParser:
    """
    Pratt Parser 实现
    """
    def __init__(self):
        self.lexer = ExprLexer()
        self.tokens = []
        self.pos = 0

    def tokenize(self, text):
        self.tokens = self.lexer.tokenize_expr(text)
        self.tokens.append(ExprToken("EOF", ""))  # 结束标记
        self.pos = 0

    def next(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def peek(self):
        return self.tokens[self.pos]

    def parse(self, text):
        self.tokenize(text)
        return self.parse_expr(0)

    # === Pratt Parser ===
    bp_table = {
        "(": 100,  # call
        "*": 50, "/": 50,
        "+": 40, "-": 40,
        "==": 30, "!=": 30, "<": 30, "<=": 30, ">": 30, ">=": 30,
        "in": 25,
        "and": 20,
        "or": 10,
    }

    def lbp(self, tok):
        return self.bp_table.get(tok.value, 0)

    def parse_expr(self, rbp):
        t = self.next()

        # prefix
        if t.kind == "NUMBER":
            left = {"type": "number", "value": t.value}
        elif t.kind == "STRING":
            left = {"type": "string", "value": t.value}
        elif t.kind == "IDENT":
            left = {"type": "var", "name": t.value}
        elif t.value == "(":
            left = self.parse_expr(0)
            self.next()  # ')'
        elif t.value in ("-", "not", "!"):
            right = self.parse_expr(100)
            left = {"type": "unary", "op": t.value, "rhs": right}

        # list literal: [expr, expr, ...]
        elif t.kind == "LBRACK":
            items = []

            # empty list: []
            if self.peek().kind == "RBRACK":
                self.next()  # skip RBRACK
                left = {"type": "list", "items": []}
            else:
                # parse elements
                while True:
                    item = self.parse_expr(0)
                    items.append(item)

                    if self.peek().kind == "COMMA":
                        self.next()  # skip comma
                        continue

                    if self.peek().kind == "RBRACK":
                        self.next()  # skip ]
                        break

                    raise SyntaxError("Expected ',' or ']' in list literal")

                left = {"type": "list", "items": items}

        else:
            raise SyntaxError(f"Unexpected token: {t}")

        # infix
        while rbp < self.lbp(self.peek()):
            op = self.next()

            if op.value == "(":
                # function call
                args = []
                if self.peek().value != ")":
                    while True:
                        args.append(self.parse_expr(0))
                        if self.peek().value == ")":
                            break
                        self.next()  # skip comma
                self.next()  # skip ')'
                left = {"type": "call", "func": left, "args": args}

            else:
                right = self.parse_expr(self.lbp(op))
                left = {"type": "binary", "op": op.value, "left": left, "right": right}

        return left
