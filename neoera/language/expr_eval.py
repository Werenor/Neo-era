from neoera.language.builtins import BUILTINS


class ExprEvaluator:
    def __init__(self, ctx):
        self.ctx = ctx

    def eval(self, node):
        t = node["type"]

        if t == "number": return node["value"]
        if t == "string": return node["value"]
        if t == "list": return [self.eval(x) for x in node["items"]]
        if t == "var": return self.ctx.get(node["name"])

        if t == "unary":
            v = self.eval(node["rhs"])
            if node["op"] == "-": return -float(v)
            if node["op"] in ("not", "!"): return not self.to_bool(v)

        if node["type"] == "list":
            return [self.eval(item) for item in node["items"]]

        if t == "binary":
            l = self.eval(node["left"])
            r = self.eval(node["right"])
            return self.eval_binary(node["op"], l, r)

        if t == "call":
            func_name = node["func"]["name"]
            args = [self.eval(a) for a in node["args"]]
            if func_name not in BUILTINS:
                raise RuntimeError(f"Unknown builtin: {func_name}")
            return BUILTINS[func_name](*args)

        raise RuntimeError(f"Unknown expr node: {t}")

    def eval_binary(self, op, l, r):
        if op == "+": return l + r
        if op == "-": return l - r
        if op == "*": return l * r
        if op == "/": return l / r

        if op == "==": return l == r
        if op == "!=": return l != r
        if op == "<": return l < r
        if op == ">": return l > r
        if op == "<=": return l <= r
        if op == ">=": return l >= r

        if op == "and": return self.to_bool(l) and self.to_bool(r)
        if op == "or":  return self.to_bool(l) or self.to_bool(r)

        if op == "in": return l in r
        raise RuntimeError(f"Unknown op: {op}")

    def to_bool(self, v):
        if isinstance(v, str): return v != ""
        if isinstance(v, (int, float)): return v != 0
        return bool(v)
