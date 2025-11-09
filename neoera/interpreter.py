# /neoera/interpreter.py
"""
Neo-era Script Interpreter v2.2
特性：
- 完整支持 text / echo / set / if / else / choice
- 自动修正字符串条件判断
- 支持变量内插值 "你好，{player}"
- 稳定兼容 parser v2 语法结构
"""

from neoera import renderer_gui as renderer
import re


class Interpreter:
    def __init__(self, ctx):
        self.ctx = ctx

    # ============================================================
    # 主执行入口
    # ============================================================
    def execute(self, ast):
        for statement in ast:
            self.execute_statement(statement)

    # ============================================================
    # 分派执行语句
    # ============================================================
    def execute_statement(self, statement):
        stype = statement.get("type")

        if stype == "echo":
            self.execute_echo(statement)
        elif stype == "text":
            self.execute_text(statement)
        elif stype == "choice":
            self.execute_choice(statement)
        elif stype == "set":
            self.execute_set(statement)
        elif stype == "if":
            self.execute_if(statement)
        else:
            print(f"[WARN] 未知语句类型: {stype}")

    # ============================================================
    # echo 显式输出
    # ============================================================
    def execute_echo(self, statement):
        expr = statement["expression"]
        text = expr["value"] if isinstance(expr, dict) else str(expr)
        text = self.interpolate(text)
        renderer.queue_echo(text)

    # ============================================================
    # text 隐式输出
    # ============================================================
    def execute_text(self, statement):
        text = statement.get("text", "")
        text = self.interpolate(text)
        renderer.queue_echo(text)

    # ============================================================
    # choice 选项
    # ============================================================
    def execute_choice(self, statement):
        options = statement.get("options", [])
        if not options:
            return
        renderer.queue_choice(options)
        result = renderer.wait_for_choice()
        self.ctx.set("choice", result)
        renderer.queue_echo(f"[玩家选择] -> {options[result]}")

    # ============================================================
    # set 赋值
    # ============================================================
    def execute_set(self, statement):
        name = statement.get("name")
        expr = statement.get("expr")

        try:
            # 尝试计算表达式
            value = eval(expr, {}, dict(self.ctx))
        except Exception:
            value = expr.strip('"')
        self.ctx.set(name, value)

    # ============================================================
    # if 条件分支
    # ============================================================
    def execute_if(self, statement):
        condition = statement.get("condition", "").strip()
        result = False

        # 直接以 ctx 为局部变量作用域进行 eval
        try:
            result = bool(eval(condition, {}, self.ctx))
        except Exception as e:
            print(f"[WARN] 条件表达式错误：{condition} ({e})")
            result = False

        # 执行对应分支
        if result:
            self.execute(statement.get("then", []))
        else:
            self.execute(statement.get("else", []))

    # ============================================================
    # 内插变量，如 "你好，{player}"
    # ============================================================
    def interpolate(self, text: str) -> str:
        def replace_var(match):
            var_name = match.group(1)
            return str(self.ctx.get(var_name, f"{{{var_name}}}"))
        return re.sub(r"\{([A-Za-z_][A-Za-z0-9_]*)\}", replace_var, text)
