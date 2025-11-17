# neoera/language/expr_eval.py

from neoera.language.builtins import BUILTINS


class ExprEvaluator:
    def __init__(self, context):
        self.ctx = context

    # --------------------------
    # Main API
    # --------------------------
    def eval(self, node):
        t = node["type"]

        if t == "number":
            return node["value"]
        if t == "string":
            return node["value"]
        if t == "var":
            return self.ctx.get(node["name"])
        if t == "list":
            return [self.eval(i) for i in node["items"]]

        if t == "unary":
            return self.eval_unary(node)

        if t == "binary":
            return self.eval_binary(node)

        if t == "call":
            return self.eval_call(node)

        raise RuntimeError(f"Unknown expr type: {t}")

    # --------------------------
    # Unary
    # --------------------------
    def eval_unary(self, node):
        op = node["op"]
        v = self.eval(node["rhs"])

        if op in ("-",):
            return -float(v)
        if op in ("not", "!"):
            return not self.to_bool(v)

        raise RuntimeError(f"Unknown unary op: {op}")

    # --------------------------
    # Binary
    # --------------------------
    def eval_binary(self, node):
        op = node["op"]
        l = self.eval(node["left"])
        r = self.eval(node["right"])

        # arithmetic
        if op == "+": return l + r
        if op == "-": return l - r
        if op == "*": return l * r
        if op == "/": return l / r

        # comparisons
        if op == "==": return l == r
        if op == "!=": return l != r
        if op == "<": return l < r
        if op == "<=": return l <= r
        if op == ">": return l > r
        if op == ">=": return l >= r

        # logic
        if op == "and": return self.to_bool(l) and self.to_bool(r)
        if op == "or": return self.to_bool(l) or self.to_bool(r)

        # in
        if op == "in": return l in r
        if op == "not in": return l not in r

        raise RuntimeError(f"Unknown binary op: {op}")

    # --------------------------
    # Function call
    # --------------------------
    def eval_call(self, node):
        func_name = node["func"]["name"]
        args = [self.eval(a) for a in node["args"]]

        if func_name not in BUILTINS:
            raise RuntimeError(f"Unknown function: {func_name}")

        return BUILTINS[func_name](*args)

    # --------------------------
    # Helper
    # --------------------------
    def to_bool(self, v):
        if isinstance(v, str):
            return v != ""
        if isinstance(v, (int, float)):
            return v != 0
        return bool(v)
