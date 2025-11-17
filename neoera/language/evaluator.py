# neoera/language/evaluator.py

class Evaluator:
    def __init__(self, ctx):
        """
        ctx 必须提供 ctx.get(name) 方法
        """
        self.ctx = ctx

    def eval(self, node):
        """入口：根据节点类型选择对应方法"""
        ntype = node.get("type")

        if ntype == "number":
            return node["value"]

        if ntype == "string":
            return node["value"]

        if ntype == "bool":
            return node["value"]

        if ntype == "variable":
            return self.ctx.get(node["name"])

        if ntype == "unary":
            return self._eval_unary(node)

        if ntype == "binary":
            return self._eval_binary(node)

        if ntype == "compare":
            return self._eval_compare(node)

        raise RuntimeError(f"无法求值的节点类型: {ntype}")

    # -------------------------------------
    #   单目运算：-x +x
    # -------------------------------------
    def _eval_unary(self, node):
        op = node["op"]
        v = self.eval(node["expr"])

        if op == "+":
            return +v
        elif op == "-":
            return -v
        else:
            raise RuntimeError(f"未知 unary 运算符: {op}")

    # -------------------------------------
    #   数学二元运算： + - * /
    # -------------------------------------
    def _eval_binary(self, node):
        op = node["op"]
        left = self.eval(node["left"])
        right = self.eval(node["right"])

        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        elif op == "/":
            return left / right
        else:
            raise RuntimeError(f"未知 binary 运算符: {op}")

    # -------------------------------------
    #   比较：== != < > <= >=
    # -------------------------------------
    def _eval_compare(self, node):
        op = node["op"]
        left = self.eval(node["left"])
        right = self.eval(node["right"])

        if op == "==":
            return left == right
        elif op == "!=":
            return left != right
        elif op == "<":
            return left < right
        elif op == ">":
            return left > right
        elif op == "<=":
            return left <= right
        elif op == ">=":
            return left >= right

        raise RuntimeError(f"未知比较运算符: {op}")
