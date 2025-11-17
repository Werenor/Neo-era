# neoera/language/parser.py

from neoera.language.lexer import Lexer
from neoera.language.expr_parser import ExprParser


class Parser:
    def __init__(self):
        self.lexer = Lexer()
        self.expr = ExprParser()

    def parse_file(self, path):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return self.parse_lines(lines)

    def parse_lines(self, lines):
        stmts = []
        stack = []

        for raw in lines:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue

            tok = self.lexer.tokenize_line(line)
            if not tok:
                continue

            cmd = tok[0]

            # ----------------------------
            # echo / implicit echo
            # ----------------------------
            if cmd == "echo":
                expr = self.expr.parse(" ".join(tok[1:]))
                stmts.append({"type": "echo", "expr": expr})
                continue

            if cmd == "text":
                text = line.split(" ", 1)[1]
                expr = {"type": "string", "value": text}
                stmts.append({"type": "echo", "expr": expr})
                continue

            # ----------------------------
            # set
            # ----------------------------
            if cmd == "set":
                var = tok[1]
                expr = self.expr.parse(" ".join(tok[3:]))
                stmts.append({"type": "set", "name": var, "expr": expr})
                continue

            # ----------------------------
            # if
            # ----------------------------
            if cmd == "if":
                condition = self.expr.parse(" ".join(tok[1:]))
                node = {"type": "if", "condition": condition, "then": [], "else": []}
                stmts.append(node)
                stack.append(node)
                continue

            if cmd == "elseif":
                condition = self.expr.parse(" ".join(tok[1:]))
                node = stack[-1]
                node.setdefault("elseif", []).append({"condition": condition, "then": []})
                continue

            if cmd == "else":
                stack[-1].setdefault("else", [])
                continue

            if cmd == "endif":
                stack.pop()
                continue

            # ----------------------------
            # choice
            # ----------------------------
            if cmd == "choice":
                opts = [s.strip('"') for s in tok[1:]]
                stmts.append({"type": "choice", "options": opts})
                continue

            # ----------------------------
            # simple commands
            # ----------------------------
            if cmd in ("bg", "bgm", "stop_bgm"):
                stmts.append({"type": cmd, "path": " ".join(tok[1:])})
                continue

            if cmd in ("sprite_show", "show_sprite"):
                stmts.append({"type": "sprite_show", "path": tok[1], "pos": tok[2] if len(tok) > 2 else "center"})
                continue

            if cmd in ("sprite_hide", "hide_sprite"):
                stmts.append({"type": "sprite_hide", "path": tok[1]})
                continue

        return stmts
